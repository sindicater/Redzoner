<script>
  import { createEventDispatcher } from 'svelte';
  
  export let type = 'sidebar'; // 'sidebar', 'top', or 'bottom'
  const dispatch = createEventDispatcher();

  function navigate(page) {
    console.log('Dispatching navigate event for:', page);
    dispatch('navigate', { page });
  }
</script>

<style>
  .sidebar-nav {
    display: flex;
    flex-direction: column;
    padding: 20px;
  }

  .top-nav {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .bottom-nav {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  .nav-item {
    margin: 10px 0;
    font-size: 1.2em;
    cursor: pointer;
    color: black; /* Black text for top/bottom nav */
  }

  .sidebar-nav .nav-item {
    color: white; /* White text for sidebar */
  }

  .nav-title {
    font-size: 1.9em;
    font-weight: bold;
    margin-bottom: 20px;
    background: linear-gradient(45deg, #ff0000, #ffc371, #FFE9C4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .bottom-nav .nav-item {
    font-size: 1em;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
  }

  /* Hide title in bottom nav */
  .bottom-nav .nav-title {
    display: none;
  }
</style>

{#if type === 'sidebar'}
  <div class="sidebar-nav">
    <div class="nav-title">Redzoner</div>
    <div class="nav-item" on:click={() => navigate('home')}>
      <i class="fas fa-home"></i> Home
    </div>
    <div class="nav-item" on:click={() => navigate('crimeMap')}>
      <i class="fas fa-map-marker-alt"></i> Crime Map
    </div>
    <div class="nav-item" on:click={() => navigate('analysis')}>
      <i class="fas fa-chart-bar"></i> Analysis
    </div>
    <div class="nav-item" on:click={() => navigate('notifications')}>
      <i class="fas fa-bell"></i> Notifications
    </div>
  </div>
{:else if type === 'top'}
  <div class="top-nav">
    <div class="nav-title">Redzoner</div>
  </div>
{:else if type === 'bottom'}
  <div class="bottom-nav">
    <div class="nav-title">Redzoner</div>
    <div class="nav-item" on:click={() => navigate('home')}>
      <i class="fas fa-home"></i> Home
    </div>
    <div class="nav-item" on:click={() => navigate('crimeMap')}>
      <i class="fas fa-map-marker-alt"></i> Map
    </div>
    <div class="nav-item" on:click={() => navigate('analysis')}>
      <i class="fas fa-chart-bar"></i> Analysis
    </div>
    <div class="nav-item" on:click={() => navigate('notifications')}>
      <i class="fas fa-bell"></i> Alerts
    </div>
  </div>
{/if}