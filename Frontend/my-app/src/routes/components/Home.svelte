<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  function goToReports() {
    dispatch('navigate', { page: 'reports' });
  }
</script>

<style>
  .home {
    padding: 20px; /* Reduced padding for mobile */
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f4f4f9;
    min-height: 100vh; /* Ensure it takes full height */
  }

  .hero {
    font-size: 1.5em; /* Smaller font size for mobile */
    margin-bottom: 20px;
    color: #333;
    text-align: center;
    line-height: 1.2; /* Better readability */
  }

  .card-container {
    display: flex;
    flex-direction: column; /* Stack cards vertically on mobile */
    gap: 15px; /* Reduced gap for mobile */
    width: 100%;
    margin-top: 15px;
  }

  .card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 15px; /* Reduced padding */
    text-align: center;
    transition: transform 0.3s ease;
  }

  .card:hover {
    transform: translateY(-5px); /* Hover effect retained for desktop */
  }

  .card img {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin-bottom: 10px;
  }

  .card h3 {
    color: #007BFF;
    margin-bottom: 8px;
    font-weight: bold;
    font-size: 1.2em; /* Slightly smaller for mobile */
  }

  .card p {
    color: #666;
    font-size: 0.9em; /* Smaller text for mobile */
    line-height: 1.4;
  }

  .cta-button {
    background-color: #007BFF;
    color: white;
    padding: 12px 25px; /* Slightly smaller padding */
    border-radius: 6px;
    border: none; /* Remove default button border */
    text-decoration: none;
    margin-top: 15px;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .cta-button:hover {
    background-color: #0056b3;
  }

  .report-button-container {
    margin-bottom: 20px;
    width: 100%;
    text-align: center;
  }

  /* Desktop layout */
  @media (min-width: 768px) {
    .home {
      padding: 40px; /* Original padding for desktop */
    }

    .hero {
      font-size: 2em; /* Original size for desktop */
    }

    .card-container {
      display: grid;
      grid-template-columns: repeat(4, 1fr); /* 4 columns for desktop */
      gap: 20px; /* Original gap */
      max-width: 1200px;
    }

    .card {
      padding: 20px; /* Original padding */
    }

    .card h3 {
      font-size: 1.3em; /* Slightly larger for desktop */
    }

    .card p {
      font-size: 1em; /* Original size */
    }

    .cta-button {
      padding: 15px 30px; /* Original padding */
      font-size: 1.1em;
    }
  }
</style>

<div class="home">
  <div class="hero">
    Welcome to Redzoner – Empowering Communities for Safer Neighborhoods
  </div>

  <div class="report-button-container">
    <button class="cta-button" on:click={goToReports}>Report an Incident</button>
  </div>

  <div class="card-container">
    <div class="card">
      <img src="redzone.jpeg" alt="About Redzoner">
      <h3>About Redzoner</h3>
      <p>Redzoner is a community-driven platform designed to help you stay informed about crime in your area. Our mission is to empower communities by providing tools to report, analyze, and stay aware of crime activities.</p>
    </div>

    <div class="card">
      <img src="crimezone.jpeg" alt="Find Crime Areas">
      <h3>Find Crime Areas</h3>
      <p>Explore our interactive crime map to identify areas with reported criminal activities. Stay alert and informed to keep yourself and your loved ones safe.</p>
    </div>

    <div class="card">
      <img src="crimerate.jpeg" alt="Analyze Crime Rates">
      <h3>Analyze Crime Rates</h3>
      <p>Dive into our analytics tools to understand crime trends in your neighborhood. Make data-driven decisions to enhance your community's safety measures.</p>
    </div>

    <div class="card">
      <img src="whistleblower.png" alt="Make a Report">
      <h3>Make a Report</h3>
      <p>Contribute to community safety by reporting any suspicious or criminal activities you witness. Your reports help us build a safer environment for everyone.</p>
    </div>
  </div>
</div>