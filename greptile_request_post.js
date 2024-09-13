require('dotenv').config();

const greptile_api_key = process.env.greptile_api_key;
const github_token = process.env.PAT;

const repository_payload = {
    remote: "github",
    repository: "pandas-dev/pandas"
};

fetch('https://api.greptile.com/v2/repositories', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${greptile_api_key}`,
        'X-Github-Token': github_token,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(repository_payload)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));