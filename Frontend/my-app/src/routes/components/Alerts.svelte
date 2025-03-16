<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  let crimeRateChart;
  let incidentTypeChart;
  let timeOfDayChart;
  let crimeHistogramChart;
  let safeAreas = [];
  let unsafeAreas = [];
  let crimeTimes = [];

  onMount(async () => {
    // Time of Day Incidents Chart (Pie Chart)
    const timeOfDayCtx = document.getElementById('timeOfDayChart').getContext('2d');
    timeOfDayChart = new Chart(timeOfDayCtx, {
      type: 'pie',
      data: {
        labels: ['Morning', 'Afternoon', 'Evening', 'Night'],
        datasets: [{
          label: 'Incidents by Time of Day',
          data: [30, 25, 20, 25],
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
          }
        }
      }
    });

    // Crime Rate Over Time Chart (Line Chart)
    const crimeRateCtx = document.getElementById('crimeRateChart').getContext('2d');
    crimeRateChart = new Chart(crimeRateCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Crime Rate',
          data: [12, 19, 3, 5, 2, 3, 7],
          borderColor: '#FF6384',
          fill: false,
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });

    // Incident Type Distribution Chart (Bar Chart)
    const incidentTypeCtx = document.getElementById('incidentTypeChart').getContext('2d');
    incidentTypeChart = new Chart(incidentTypeCtx, {
      type: 'bar',
      data: {
        labels: ['Theft', 'Assault', 'Burglary', 'Vandalism'],
        datasets: [{
          label: 'Number of Incidents',
          data: [12, 19, 3, 5],
          backgroundColor: '#36A2EB',
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });

    // Crime Histogram Chart (Histogram)
    const crimeHistogramCtx = document.getElementById('crimeHistogramChart').getContext('2d');
    crimeHistogramChart = new Chart(crimeHistogramCtx, {
      type: 'bar',
      data: {
        labels: ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100'],
        datasets: [{
          label: 'Number of Crimes',
          data: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
          backgroundColor: '#FFCE56',
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });

    // Fetch data for charts
    await fetchSafeAreas();
    await fetchUnsafeAreas();
    await fetchCrimeTimes();
    await fetchCrimeRateData();
    await fetchIncidentTypeData();
    await fetchCrimeHistogramData();
  });

  // Function to fetch safe areas
  async function fetchSafeAreas() {
    const response = await fetch('http://127.0.0.1:5000/safe-areas');
    if (response.ok) {
      safeAreas = await response.json();
      console.log("Safe areas fetched:", safeAreas);
    } else {
      console.error('Error fetching safe areas:', response.statusText);
    }
  }

  // Function to fetch unsafe areas
  async function fetchUnsafeAreas() {
    const response = await fetch('http://127.0.0.1:5000/unsafe-areas');
    if (response.ok) {
      unsafeAreas = await response.json();
      console.log("Unsafe areas fetched:", unsafeAreas);
    } else {
      console.error('Error fetching unsafe areas:', response.statusText);
    }
  }

  // Function to fetch crime times
  async function fetchCrimeTimes() {
    const response = await fetch('http://127.0.0.1:5000/crime-time-data');
    if (response.ok) {
      crimeTimes = await response.json();
      console.log("Crime times fetched:", crimeTimes);
      updateTimeOfDayChart(crimeTimes);
    } else {
      console.error('Error fetching crime times:', response.statusText);
    }
  }

  // Function to update the Time of Day Chart
  function updateTimeOfDayChart(crimeTimes) {
    const morning = crimeTimes.filter(time => {
      const hour = new Date(time).getHours();
      return hour >= 6 && hour < 12;
    }).length;

    const afternoon = crimeTimes.filter(time => {
      const hour = new Date(time).getHours();
      return hour >= 12 && hour < 18;
    }).length;

    const evening = crimeTimes.filter(time => {
      const hour = new Date(time).getHours();
      return hour >= 18 && hour < 24;
    }).length;

    const night = crimeTimes.filter(time => {
      const hour = new Date(time).getHours();
      return hour >= 0 && hour < 6;
    }).length;

    timeOfDayChart.data.datasets[0].data = [morning, afternoon, evening, night];
    timeOfDayChart.update();
  }

  // Function to fetch crime rate data
  async function fetchCrimeRateData() {
    const response = await fetch('http://127.0.0.1:5000/data');
    if (response.ok) {
      const data = await response.json();
      const crimeRates = data.map(entry => entry.crime_time);
      console.log("Crime rate data fetched:", crimeRates);
      updateCrimeRateChart(crimeRates);
    } else {
      console.error('Error fetching crime rate data:', response.statusText);
    }
  }

  // Function to update the Crime Rate Chart
  function updateCrimeRateChart(crimeRates) {
    const monthlyCrimeCounts = {};
    crimeRates.forEach(time => {
      const month = new Date(time).toLocaleString('default', { month: 'short' });
      monthlyCrimeCounts[month] = (monthlyCrimeCounts[month] || 0) + 1;
    });

    const labels = Object.keys(monthlyCrimeCounts);
    const data = Object.values(monthlyCrimeCounts);

    crimeRateChart.data.labels = labels;
    crimeRateChart.data.datasets[0].data = data;
    crimeRateChart.update();
  }

  // Function to fetch incident type data
  async function fetchIncidentTypeData() {
    const response = await fetch('http://127.0.0.1:5000/data');
    if (response.ok) {
      const data = await response.json();
      const incidentTypes = data.map(entry => entry.crime_type);
      console.log("Incident type data fetched:", incidentTypes);
      updateIncidentTypeChart(incidentTypes);
    } else {
      console.error('Error fetching incident type data:', response.statusText);
    }
  }

  // Function to update the Incident Type Chart
  function updateIncidentTypeChart(incidentTypes) {
    const typeCounts = {};
    incidentTypes.forEach(type => {
      typeCounts[type] = (typeCounts[type] || 0) + 1;
    });

    const labels = Object.keys(typeCounts);
    const data = Object.values(typeCounts);

    incidentTypeChart.data.labels = labels;
    incidentTypeChart.data.datasets[0].data = data;
    incidentTypeChart.update();
  }

  // Function to fetch crime histogram data
  async function fetchCrimeHistogramData() {
    const response = await fetch('http://127.0.0.1:5000/data');
    if (response.ok) {
      const data = await response.json();
      const crimeTimes = data.map(entry => entry.crime_time);
      console.log("Crime histogram data fetched:", crimeTimes);
      updateCrimeHistogramChart(crimeTimes);
    } else {
      console.error('Error fetching crime histogram data:', response.statusText);
    }
  }

  // Function to update the Crime Histogram Chart
  function updateCrimeHistogramChart(crimeTimes) {
    const histogramData = Array(10).fill(0);
    crimeTimes.forEach(time => {
      const hour = new Date(time).getHours();
      const bin = Math.floor(hour / 10);
      histogramData[bin]++;
    });

    crimeHistogramChart.data.datasets[0].data = histogramData;
    crimeHistogramChart.update();
  }
</script>

<style>
  .alerts {
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .search-container {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }

  .search-bar {
    width: 100%;
    max-width: 600px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1em;
  }

  .search-bar::placeholder {
    color: #aaa;
  }

  .card-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    width: 100%;
  }

  .card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
    transition: transform 0.3s ease;
  }

  .card:hover {
    transform: translateY(-5px);
  }

  .card-title {
    font-size: 1.2em;
    margin-bottom: 10px;
    color: #333;
  }

  .chart-container {
    position: relative;
    height: 250px;
  }

  .list-container {
    max-height: 250px;
    overflow-y: auto;
  }

  .list-item {
    padding: 8px;
    border-bottom: 1px solid #eee;
  }

  .list-item:last-child {
    border-bottom: none;
  }

  @media (min-width: 768px) {
    .card {
      width: calc(33.333% - 20px);
    }
  }
</style>

<div class="alerts">
  <div class="search-container">
    <input type="text" class="search-bar" placeholder="Search by area..." />
  </div>

  <div class="card-grid">
    <div class="card">
      <div class="card-title">Incidents by Time of Day</div>
      <div class="chart-container">
        <canvas id="timeOfDayChart"></canvas>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Crime Rate Over Time</div>
      <div class="chart-container">
        <canvas id="crimeRateChart"></canvas>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Incident Type Distribution</div>
      <div class="chart-container">
        <canvas id="incidentTypeChart"></canvas>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Safest Areas in Kenya</div>
      <div class="list-container">
        {#each safeAreas as area}
          <div class="list-item">{area}</div>
        {/each}
      </div>
    </div>

    <div class="card">
      <div class="card-title">Most Unsafe Areas in Kenya</div>
      <div class="list-container">
        {#each unsafeAreas as area}
          <div class="list-item">{area}</div>
        {/each}
      </div>
    </div>

    <div class="card">
      <div class="card-title">Crime Histogram</div>
      <div class="chart-container">
        <canvas id="crimeHistogramChart"></canvas>
      </div>
    </div>
  </div>
</div>
