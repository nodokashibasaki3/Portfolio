// function typeWriter(text, n) {
//     if (n < (text.length)) {
//         document.getElementById('typewriter').innerHTML = text.substring(0, n+1);
//         n++;
//         // Change the rate of typing by adjusting the timeout
//         setTimeout(function() {
//             typeWriter(text, n)
//         }, 100);
//     }
// }

// document.getElementById('login-form').addEventListener('submit', function(event) {
//     event.preventDefault();
//     const password = document.getElementById('password').value;
//     const dashboard = document.querySelector('.dashboard');
//     const loginContainer = document.querySelector('.login-container');
    
//     if (password === "yourpassword") { // Replace with your actual password
//         loginContainer.classList.add('hidden');
//         dashboard.classList.remove('hidden'); // Show the dashboard with About, CPU, and Memory info

//         // Load CPU info
//         updateCpuInfo();

//         // Load Memory info
//         updateMemoryInfo();

//         // Optionally, if there's a need to update the About Me info dynamically, call here
//         // updateAboutInfo();

//     } else {
//         alert('Incorrect password');
//     }
// });

// function updateCpuInfo() {
//     // Generate random CPU usage data
//     const cpuUsage = (Math.random() * 100).toFixed(2); // Random CPU load percentage
//     const cpuTemp = (30 + Math.random() * 70).toFixed(2); // Random CPU temperature

//     // Update the CPU information panel
//     document.getElementById('cpuInfo').textContent = `Usage: ${cpuUsage}% - Temp: ${cpuTemp}°C`;
// }

// function updateMemoryInfo() {
//     // Generate random Memory usage data
//     const totalMemory = 16; // Assuming 16GB total memory for the example
//     const usedMemory = (Math.random() * totalMemory).toFixed(2); // Random memory usage
//     const freeMemory = (totalMemory - usedMemory).toFixed(2); // Calculate free memory

//     // Update the Memory information panel
//     document.getElementById('memoryInfo').textContent = `Used: ${usedMemory}GB - Free: ${freeMemory}GB`;
// }

// // Initialize the panels with random data on page load
// document.addEventListener('DOMContentLoaded', function() {
//     updateCpuInfo();
//     updateMemoryInfo();
// });