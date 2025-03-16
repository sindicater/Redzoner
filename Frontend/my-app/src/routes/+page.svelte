<script>
  import Nav from './Nav.svelte';
  import Home from './components/Home.svelte';
  import CrimeMap from './components/CrimeMap.svelte';
  import Analysis from './components/Alerts.svelte';
  import Notifications from './components/Notifications.svelte';
  import Reports from './components/Reports.svelte';

  let currentPage = 'home';

  function navigateTo(event) {
    console.log('Navigating to:', event.detail.page);
    currentPage = event.detail.page;
  }
</script>

<style>
  .container {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .content {
    flex: 1;
    padding: 20px;
    background-color: #f4f4f9;
    overflow-y: auto;
  }

  /* Desktop sidebar layout */
  @media (min-width: 768px) {
    .container {
      flex-direction: row;
    }

    .sidebar {
      width: 20%;
      background-color: #000000;
      color: white;
    }

    .content {
      width: 80%;
    }

    .top-nav {
      display: none;
    }

    .bottom-nav {
      display: none;
    }
  }

  /* Mobile layout */
  @media (max-width: 767px) {
    .sidebar {
      display: none;
    }

    .top-nav {
      background-color: #f4f4f9;
      padding: 10px;
      border-bottom: 1px solid #f4f4f9;
    }

    .bottom-nav {
      background-color: #f4f4f9;
      border-top: 1px solid #f4f4f9;
      padding: 10px 0;
    }
  }
</style>

<div class="container">
  <!-- Top bar for mobile -->
  <div class="top-nav">
    <Nav type="top" on:navigate={navigateTo} />
  </div>

  <!-- Sidebar for desktop -->
  <div class="sidebar">
    <Nav type="sidebar" on:navigate={navigateTo} />
  </div>

  <!-- Main content -->
  <div class="content">
    {#if currentPage === 'home'}
      <Home on:navigate={navigateTo} />
    {:else if currentPage === 'crimeMap'}
      <CrimeMap />
    {:else if currentPage === 'analysis'}
      <Analysis />
    {:else if currentPage === 'notifications'}
      <Notifications />
    {:else if currentPage === 'reports'}
      <Reports />
    {/if}
  </div>

  <!-- Bottom nav for mobile -->
  <div class="bottom-nav">
    <Nav type="bottom" on:navigate={navigateTo} />
  </div>
</div>