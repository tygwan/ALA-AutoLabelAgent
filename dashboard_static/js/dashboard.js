// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    loadCategories();
    
    // Set up event listeners
    setupDragAndDrop();
});

// Load available categories
function loadCategories() {
    fetch('/api/categories')
        .then(response => response.json())
        .then(data => {
            // Categories are loaded via Jinja template
            console.log('Categories loaded:', data.categories);
        })
        .catch(error => console.error('Error loading categories:', error));
}

// Load a specific category
function loadCategory(category) {
    console.log('Loading category:', category);
    
    // Load support set
    fetch(`/api/support-set/${category}`)
        .then(response => response.json())
        .then(data => {
            displaySupportSet(data.images);
        })
        .catch(error => console.error('Error loading support set:', error));
    
    // Load refined dataset
    fetch(`/api/refined-dataset/${category}`)
        .then(response => response.json())
        .then(data => {
            displayRefinedDataset(data.images);
            updateAnalytics(data.stats);
        })
        .catch(error => console.error('Error loading refined dataset:', error));
}

// Display support set images
function displaySupportSet(images) {
    const gallery = document.getElementById('support-set-gallery');
    gallery.innerHTML = '';
    
    images.forEach(image => {
        const card = document.createElement('div');
        card.className = 'image-card';
        card.setAttribute('draggable', 'true');
        card.setAttribute('data-path', image.path);
        card.setAttribute('data-class', image.class);
        
        const img = document.createElement('img');
        img.src = `/api/image?path=${encodeURIComponent(image.path)}`;
        img.alt = image.class;
        
        const info = document.createElement('div');
        info.className = 'info';
        info.textContent = image.class;
        
        card.appendChild(img);
        card.appendChild(info);
        gallery.appendChild(card);
        
        // Set up drag events
        card.addEventListener('dragstart', handleDragStart);
    });
}

// Display refined dataset images
function displayRefinedDataset(images) {
    const gallery = document.getElementById('refined-dataset-gallery');
    gallery.innerHTML = '';
    
    images.forEach(image => {
        const card = document.createElement('div');
        card.className = 'image-card';
        card.setAttribute('data-path', image.path);
        card.setAttribute('data-class', image.class);
        card.setAttribute('data-id', image.id);
        
        const img = document.createElement('img');
        img.src = `/api/image?path=${encodeURIComponent(image.path)}`;
        img.alt = image.class;
        
        const info = document.createElement('div');
        info.className = 'info';
        info.innerHTML = `
            <div>Class: ${image.class}</div>
            <div>Confidence: ${image.confidence || 'N/A'}</div>
        `;
        
        card.appendChild(img);
        card.appendChild(info);
        gallery.appendChild(card);
    });
}

// Update analytics section
function updateAnalytics(stats) {
    // Update class distribution chart
    const ctx = document.getElementById('class-distribution-chart').getContext('2d');
    
    if (window.classChart) {
        window.classChart.destroy();
    }
    
    window.classChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(stats.class_distribution),
            datasets: [{
                label: 'Class Distribution',
                data: Object.values(stats.class_distribution),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
    
    // Update statistics
    const statsContainer = document.querySelector('.stats-container');
    statsContainer.innerHTML = '';
    
    // Add total objects stat
    const totalCard = document.createElement('div');
    totalCard.className = 'stat-card';
    totalCard.innerHTML = `
        <h3>Total Objects</h3>
        <p>${stats.total_objects}</p>
    `;
    statsContainer.appendChild(totalCard);
    
    // Add average confidence stat
    const confidenceCard = document.createElement('div');
    confidenceCard.className = 'stat-card';
    confidenceCard.innerHTML = `
        <h3>Avg. Confidence</h3>
        <p>${stats.average_confidence ? stats.average_confidence.toFixed(2) : 'N/A'}</p>
    `;
    statsContainer.appendChild(confidenceCard);
    
    // Add method selection stats
    const methodCard = document.createElement('div');
    methodCard.className = 'stat-card';
    methodCard.innerHTML = `
        <h3>Classification Method</h3>
        <p>${stats.method || 'None'}</p>
    `;
    statsContainer.appendChild(methodCard);
}

// Set up drag and drop for reclassification
function setupDragAndDrop() {
    const dropZones = document.querySelectorAll('.gallery');
    
    dropZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('drop', handleDrop);
    });
}

function handleDragStart(event) {
    event.dataTransfer.setData('text/plain', JSON.stringify({
        path: event.target.getAttribute('data-path'),
        class: event.target.getAttribute('data-class'),
        id: event.target.getAttribute('data-id')
    }));
}

function handleDragOver(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
}

function handleDrop(event) {
    event.preventDefault();
    
    const data = JSON.parse(event.dataTransfer.getData('text/plain'));
    const targetGallery = event.currentTarget;
    const targetClass = targetGallery.parentElement.querySelector('h2').textContent;
    
    console.log('Dropped:', data);
    console.log('Target gallery:', targetGallery.id);
    
    if (targetGallery.id === 'refined-dataset-gallery') {
        // Reclassify object
        const method = document.getElementById('classification-method').value;
        
        fetch('/api/reclassify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image_id: data.id,
                source_class: data.class,
                target_class: targetClass,
                method: method
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log('Reclassification result:', result);
            // Reload category to reflect changes
            const currentCategory = document.querySelector('.category-card.active').getAttribute('data-category');
            loadCategory(currentCategory);
        })
        .catch(error => console.error('Error reclassifying object:', error));
    }
}

// Apply classification method
function applyClassification() {
    const method = document.getElementById('classification-method').value;
    const activeCategory = document.querySelector('.category-card.active');
    
    if (!activeCategory) {
        alert('Please select a category first');
        return;
    }
    
    const category = activeCategory.getAttribute('data-category');
    
    fetch('/api/apply-classification', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            category: category,
            method: method
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log('Classification applied:', result);
        // Reload category to reflect changes
        loadCategory(category);
    })
    .catch(error => console.error('Error applying classification:', error));
}
