document.getElementById('homeschoolForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const age = document.getElementById('age').value;
    const schoolYear = document.getElementById('schoolYear').value;
    const subject = document.getElementById('subject').value;
    const topic = document.getElementById('topic').value;
    const aspiration = document.getElementById('aspiration').value;

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ age, schoolYear, subject, topic, aspiration }),
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('output').innerHTML = data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
