<script>
  import { onMount } from 'svelte';

  let name = '';
  let latitude = -1.286389;
  let longitude = 36.817223;
  let radius = 2000;
  let type = 'unsafe';
  let crimeType = 'burglary';
  let crimeTime = new Date().toISOString();
  let safetyStatus = false; // Default as boolean
  let placeQuery = '';

  // Function to get the user's current location
  async function getCurrentLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          latitude = position.coords.latitude;
          longitude = position.coords.longitude;
        },
        error => {
          console.error('Error getting location:', error);
        }
      );
    } else {
      console.error('Geolocation is not supported by this browser.');
    }
  }

  // Function to geocode a place and get its coordinates
  async function geocodePlace() {
    if (!placeQuery.trim()) {
      alert('Please enter a place name.');
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:5000/geocode?place=${encodeURIComponent(placeQuery)}`);
      const data = await response.json();

      if (response.ok) {
        latitude = data.latitude;
        longitude = data.longitude;
        name = placeQuery;
      } else {
        alert('Place not found. Please try again.');
      }
    } catch (error) {
      console.error('Error fetching geocode data:', error);
      alert('Failed to retrieve location data. Please try again.');
    }
  }

  // Function to submit the report
  async function submitReport() {
    const data = {
      name,
      coords: { latitude, longitude },
      radius,
      type,
      crime_type: crimeType,
      crime_time: crimeTime,
      safety_status: safetyStatus // Boolean value
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        alert('Report submitted successfully!');
      } else {
        alert('Failed to submit report.');
      }
    } catch (error) {
      console.error('Error submitting report:', error);
    }
  }

  onMount(() => {
    getCurrentLocation();
  });
</script>

<style>
  .reports-container {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  }

  .card h3 {
    margin-top: 0;
    font-size: 1.2em;
    color: #333;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
  }

  .form-group input,
  .form-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1em;
  }

  .form-group button {
    background-color: #007BFF;
    color: white;
    padding: 15px 20px;
    border: none;
    border-radius: 8px;
    font-size: 1em;
    cursor: pointer;
    align-self: flex-end;
    transition: background-color 0.3s ease;
  }

  .form-group button:hover {
    background-color: #0056b3;
  }

  .submit-button {
    grid-column: span 1;
    text-align: center;
  }

  .submit-button button {
    background-color: #28a745;
    font-size: 1.2em;
    padding: 15px 30px;
    border-radius: 10px;
  }

  .submit-button button:hover {
    background-color: #218838;
  }

  @media (min-width: 769px) {
    .reports-container {
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    }

    .submit-button {
      grid-column: span 3;
    }
  }
</style>

<div class="reports-container">
  <div class="card">
    <h3>Search for a Place</h3>
    <div class="form-group">
      <label for="placeQuery">Place Name</label>
      <input
        type="text"
        id="placeQuery"
        bind:value={placeQuery}
        placeholder="Enter place name"
      />
      <button on:click={geocodePlace}>Search</button>
    </div>
  </div>

  <div class="card">
    <h3>Crime Details</h3>
    <div class="form-group">
      <label for="crimeType">Crime Type</label>
      <select id="crimeType" bind:value={crimeType}>
        <option value="burglary">Burglary</option>
        <option value="theft">Theft</option>
        <option value="assault">Assault</option>
        <option value="vandalism">Vandalism</option>
      </select>
    </div>
    <div class="form-group">
      <label for="crimeTime">Crime Time</label>
      <input type="datetime-local" id="crimeTime" bind:value={crimeTime} />
    </div>
  </div>

  <div class="card">
    <h3>Area Details</h3>
    <div class="form-group">
      <label for="name">Name of Area</label>
      <input type="text" id="name" bind:value={name} placeholder="Enter area name" />
    </div>
    <div class="form-group">
      <label for="latitude">Latitude</label>
      <input type="number" id="latitude" bind:value={latitude} placeholder="Enter latitude" />
    </div>
    <div class="form-group">
      <label for="longitude">Longitude</label>
      <input type="number" id="longitude" bind:value={longitude} placeholder="Enter longitude" />
    </div>
    <div class="form-group">
      <label for="radius">Radius (meters)</label>
      <input type="number" id="radius" bind:value={radius} placeholder="Enter radius" />
    </div>
    <div class="form-group">
      <label for="safetyStatus">Safety Status</label>
      <select id="safetyStatus" bind:value={safetyStatus}>
        <option value={true}>Safe</option>
        <option value={false}>Unsafe</option>
      </select>
    </div>
  </div>

  <div class="submit-button">
    <button on:click={submitReport}>Submit Report</button>
  </div>
</div>
