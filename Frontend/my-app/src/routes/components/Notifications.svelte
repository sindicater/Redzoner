<script>
  // Example data: Replace this with actual data fetching logic
  let notifications = [
    {
      id: 1,
      type: 'area', // Type of notification
      area: 'Downtown',
      status: 'Safe',
      message: 'The area is currently safe with no reported incidents.',
      timestamp: '2023-10-25 10:30 AM'
    },
    {
      id: 2,
      type: 'area',
      area: 'Park District',
      status: 'Moderate',
      message: 'There have been a few minor incidents. Stay alert.',
      timestamp: '2023-10-25 11:15 AM'
    },
    {
      id: 3,
      type: 'area',
      area: 'Industrial Zone',
      status: 'Dangerous',
      message: 'High crime rate reported. Avoid if possible.',
      timestamp: '2023-10-25 12:00 PM'
    },
    {
      id: 4,
      type: 'friend', // Friend joining notification
      friendName: 'John Doe',
      message: 'John Doe has joined the program.',
      timestamp: '2023-10-25 09:45 AM'
    },
    {
      id: 5,
      type: 'friend',
      friendName: 'Jane Smith',
      message: 'Jane Smith has joined the program.',
      timestamp: '2023-10-25 10:00 AM'
    }
  ];

  // Function to determine the color based on status
  function getStatusColor(status) {
    switch (status) {
      case 'Safe':
        return 'green';
      case 'Moderate':
        return 'orange';
      case 'Dangerous':
        return 'red';
      default:
        return 'gray';
    }
  }
</script>

<style>
  .notifications {
    padding: 20px;
    background-color: #f4f4f9;
  }

  .notification {
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 5px;
    position: relative;
    background-color: white;
  }

  .status {
    font-weight: bold;
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 5px 10px;
    border-radius: 3px;
    color: white;
  }

  .area {
    font-size: 1.2em;
    margin-bottom: 5px;
  }

  .friend-name {
    font-size: 1.2em;
    margin-bottom: 5px;
    color: #007bff; /* Blue color for friend names */
  }

  .message {
    font-size: 1em;
    color: #555;
    margin-bottom: 10px;
  }

  .timestamp {
    font-size: 0.9em;
    color: #888;
    text-align: right;
  }
</style>

<div class="notifications">
  {#each notifications as notification}
    <div class="notification">
      {#if notification.type === 'area'}
        <!-- Area Status Notification -->
        <div class="area">{notification.area}</div>
        <div class="message">{notification.message}</div>
        <div class="status" style="background-color: {getStatusColor(notification.status)}">
          {notification.status}
        </div>
      {:else if notification.type === 'friend'}
        <!-- Friend Joining Notification -->
        <div class="friend-name">{notification.friendName}</div>
        <div class="message">{notification.message}</div>
      {/if}
      <div class="timestamp">{notification.timestamp}</div>
    </div>
  {/each}
</div>