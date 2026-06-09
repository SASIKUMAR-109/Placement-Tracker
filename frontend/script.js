const searchInput = document.getElementById("search-input");
const resultsSection = document.getElementById("results-section");
const searchBtn = document.getElementById("search-btn");
const collegeName = document.getElementById("college-name");
const collegeLocation = document.getElementById("college-location");
const collegeType = document.getElementById("college-type");
const statTotal = document.getElementById("stat-total");
const statPlaced = document.getElementById("stat-placed");
const statPct = document.getElementById("stat-pct");
const placementChart = document.getElementById("placement-chart");
const placementTable = document.getElementById("placement-table");
const tableBody = document.getElementById('table-body')
let chartInstance = null;


const disclaimerOverlay = document.getElementById('disclaimer-overlay');
const disclaimerBtn = document.getElementById('disclaimer-btn');


disclaimerBtn.addEventListener('click', function() {
    disclaimerOverlay.style.display = 'none';
});

function fillTable(data){
    tableBody.innerHTML = '';
    for (let i of data){
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${i.year}</td>
                        <td>${i.branch}</td>
                        <td>${i.total_students}</td>
                        <td>${i.students_placed}</td>
                        <td>${i.placement_pct.toFixed(1)}%</td>
                        <td>${i.median_package_lpa !== null ? i.median_package_lpa.toFixed(2) + ' LPA' : 'N/A'}</td>`
        tableBody.append(tr);
                    }
}



function displayData(data){
   resultsSection.style.display = "block";
    collegeName.textContent = data.college.college_name;
    collegeLocation.textContent = data.college.city + " ," +data.college.state;
    collegeType.textContent = data.college.college_type;
    
    let latest = data.placements[0]
    for (let i of data.placements){
        if (latest.year <i.year){
            latest = i
        }
    }



    statTotal.textContent = latest.total_students
    statPlaced.textContent = latest.students_placed
    statPct.textContent = Math.min(latest.placement_pct, 100).toFixed(1) + '%'
    drawChart(data.placements)
    fillTable(data.placements)
} 

function drawChart(placements){
    if (chartInstance !== null){
        chartInstance.destroy();
    }
    let yearGroups ={};
    for(let item of placements){
        let year = item.year;
        if (!(year in yearGroups)){
            yearGroups[year]=[];
        }
        yearGroups[year].push(item.placement_pct)
        
    }
    let labels = []
    let values = []
    for (let year of Object.keys(yearGroups).sort()){
        let sum = yearGroups[year].reduce((a, b) => a + b, 0)
        let avg = sum / yearGroups[year].length
        labels.push(year)
        values.push(Math.min(avg, 100).toFixed(1))
    }
    
    chartInstance = new Chart(placementChart, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Placement %',
            data: values,
            
            fill: true,
            tension: 0.3,
            pointRadius: 5,
            backgroundColor: 'rgba(124, 58, 237, 0.1)',
borderColor: '#7c3aed',
pointBackgroundColor: '#4c1d95',
        }]
    },
    options: {
        
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 105
            }
        }
    }
})
}


const abbreviations = {
    'iit': 'Indian Institute of Technology',
    'nit': 'National Institute of Technology',
    'iim': 'Indian Institute of Management',
    'bits': 'Birla Institute of Technology',
    'iisc': 'Indian Institute of Science'
}


function searchCollege(event){
    let searchTerm = searchInput.value.trim();
    let searchLower = searchTerm.toLowerCase();
   
    for(let i in abbreviations){
            if (searchLower.startsWith(i)){
               searchTerm = searchTerm.replace(new RegExp(i,'i'),abbreviations[i])
               break
            }
    }
    let url = "/api/college?name=";
    
    if (searchTerm === ""){
        alert("Please enter a college name.");
        return;
    }
    url+=searchTerm;
    fetch(url)
    .then(response => {
        if (!response.ok){
            throw new Error("College not found")
            
        }
       return response.json()
    })
    .then(data => {
        
        displayData(data);
        searchInput.value = '';
        searchInput.placeholder = 'Search college name...';
        
    })
    
    .catch(error => alert(error.message));
    }


searchBtn.addEventListener("click",searchCollege);

searchInput.addEventListener("keypress",function(event){
    if (event.key == "Enter"){
    searchCollege(event)
    }
});
