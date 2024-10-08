document.addEventListener("DOMContentLoaded", function() {
    fetch('http://127.0.0.1:8000/djadmin/api/profiles/')
    .then(response => response.json())
    .then(data => {
        console.log('Fetched data:', data);  // Log the data to the console

        const appsList = document.getElementById('admin_dashboard');
        appsList.innerHTML = '';  // Clear existing content

        data.forEach(app => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'item';

            // Dynamically add the image and other details
            itemDiv.innerHTML = `
          
                
                <h2>Name: ${app.username}</h2>
                <h3>Email:${app.email}</h3>
                <h4>Total Total short links :${app.Number_of_shorterned_links}</h4>
                <a href="${app.id}" class="btn btn-success">More Details </a>
                   
            `;

            appsList.appendChild(itemDiv);
        });
    })
    .catch(error => console.error('Error fetching data:', error));
});