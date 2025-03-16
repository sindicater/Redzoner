<script>
  import { onMount } from 'svelte';

  let map;
  let showAll = true;
  let showSafe = false;
  let showUnsafe = false;
  let searchQuery = '';
  let areas = [];
  let searchMarker = null;

  // Function to toggle map layers
  function toggleMap(type) {
    showAll = type === 'all';
    showSafe = type === 'safe';
    showUnsafe = type === 'unsafe';
    updateMap();
  }

  // Function to update the map based on selected filters
  function updateMap() {
    if (!map) return;

    console.log("Updating map with areas:", areas); // Log the areas being processed

    // Clear existing layers
    map.eachLayer((layer) => {
      if (layer instanceof L.Circle || layer === searchMarker) {
        map.removeLayer(layer);
      }
    });

    // Add areas based on filters
    areas.forEach((area) => {
      const [latitude, longitude] = parseCoords(area.coords);
      console.log("Adding area to map:", area.name, "with coordinates:", latitude, longitude); // Log each area being added
      if ((showAll || showSafe) && area.safety_status) {
        addAreaToMap([latitude, longitude], area.radius, 'green', '#4CAF50', 'Safe Area', area.name);
      }
      if ((showAll || showUnsafe) && !area.safety_status) {
        addAreaToMap([latitude, longitude], area.radius, 'red', '#F44336', 'High Crime Area', area.name);
      }
    });
  }

  // Function to add an area to the map
  function addAreaToMap([lat, lng], radius, color, fillColor, label, name) {
    L.circle([lat, lng], {
      color: color,
      fillColor: fillColor,
      fillOpacity: 0.5,
      radius: radius,
    })
      .addTo(map)
      .bindPopup(`<b>${name}</b><br>${label}`);
  }

  // Function to parse coordinates
  function parseCoords(coords) {
    const match = coords.match(/[-+]?\d*\.\d+|\d+/g);
    if (match) {
      return [parseFloat(match[1]), parseFloat(match[0])]; // Ensure correct order: [latitude, longitude]
    } else {
      console.error("Invalid coordinates format:", coords);
      return [0, 0];
    }
  }

  // Function to search for a location
  async function searchLocation() {
    if (searchQuery.trim() === '') return;

    // Use OpenStreetMap's Nominatim API for geocoding
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}`);
    const data = await response.json();

    if (data.length > 0) {
      const { lat, lon } = data[0];
      map.setView([lat, lon], 14); // Zoom to the searched location

      // Remove previous search marker if it exists
      if (searchMarker) {
        map.removeLayer(searchMarker);
      }

      // Add a new marker for the searched location
      searchMarker = L.marker([lat, lon]).addTo(map).bindPopup(`<b>${searchQuery}</b>`).openPopup();
      searchMarker.setStyle({ color: 'blue', fillColor: 'blue', fillOpacity: 0.5 });
    } else {
      alert('Location not found!');
    }
  }

  // Function to fetch data from the backend
  async function fetchData() {
    const response = await fetch('http://127.0.0.1:5000/map-data');
    if (response.ok) {
      areas = await response.json();
      console.log("Fetched areas:", areas); // Log the fetched areas
      updateMap();
    } else {
      console.error('Error fetching data:', response.statusText);
    }
  }

  onMount(async () => {
    // Dynamically import Leaflet only in the browser
    const L = await import('leaflet');
    await import('leaflet/dist/leaflet.css');

    // Initialize the map centered on Kenya
    map = L.map('map').setView([-1.286389, 36.817223], 12); // Centered on Nairobi

    // Add a tile layer (you can use OpenStreetMap or other tile providers)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(map);

    // Fetch data from the backend
    await fetchData();
  });
</script>

<style>
  .crime-map {
    padding: 20px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #f4f4f9;
  }

  .map-card {
    width: 100%;
    height: 65vh; /* Reduced height */
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    padding: 20px;
  }

  #map {
    width: 100%;
    height: 100%;
    border-radius: 8px;
  }

  .filter-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap; /* Allow buttons to wrap on smaller screens */
  }

  .filter-buttons button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #e0e0e0; /* Default button color */
    color: #333;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
    flex: 1; /* Allow buttons to take equal space */
  }

  .filter-buttons button:hover {
    background-color: #d0d0d0;
  }

  .filter-buttons button.active {
    background-color: #007bff; /* Active button color */
    color: white;
  }

  .filter-buttons button.active.safe {
    background-color: #4CAF50; /* Safe button color */
  }

  .filter-buttons button.active.unsafe {
    background-color: #F44336; /* Unsafe button color */
  }

  .search-bar {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap; /* Allow search bar to wrap on smaller screens */
  }

  .search-bar input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1em;
  }

  .search-bar button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: white;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .search-bar button:hover {
    background-color: #0056b3;
  }

  @media (max-width: 768px) {
    .filter-buttons {
      flex-direction: column;
      align-items: center;
    }

    .filter-buttons button {
      width: 100%;
    }

    .search-bar {
      flex-direction: column;
      align-items: center;
    }

    .search-bar input {
      width: 100%;
    }

    .search-bar button {
      width: 100%;
    }
  }
</style>

<div class="crime-map">
  <!-- Filter Buttons -->
  <div class="filter-buttons">
    <button class:active={showAll} on:click={() => toggleMap('all')}>
      All Areas
    </button>
    <button class:active={showSafe} class:safe={showSafe} on:click={() => toggleMap('safe')}>
      Safe Areas
    </button>
    <button class:active={showUnsafe} class:unsafe={showUnsafe} on:click={() => toggleMap('unsafe')}>
      Unsafe Areas
    </button>
  </div>

  <!-- Search Bar -->
  <div class="search-bar">
    <input type="text" bind:value={searchQuery} placeholder="Search for a location..." />
    <button on:click={searchLocation}>Search</button>
  </div>

  <!-- Map Card -->
  <div class="map-card">
    <div id="map"></div>
  </div>
</div>
