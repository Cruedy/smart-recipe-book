require('dotenv').config();
const fs = require('fs');
const path = require('path');

const greptile_api_key = process.env.greptile_api_key;
const github_token = process.env.PAT;
  
const queryPayload = {
    "messages": [
        {
            "id": "query-2",
            "content": `Can you check my entire codebase including in the myapp directory and write up markdown code about 
            all javascript, python, and json files that I wrote that I can put under the Code Description 
            section in my ReadMe.md?`,
            "role": "user"
        }
    ],
    "repositories": [
        {
            "remote": "github",
            "repository": "cruedy/smart-recipe-book",
            "branch": "main"
        }
    ],
    "sessionId": "readMe-session-id"
}

async function fetchData() {
    try {
        const response = await fetch('https://api.greptile.com/v2/query', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${greptile_api_key}`,
                'X-Github-Token': github_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(queryPayload)
        });

        const data = await response.json();  // Get the data as a JavaScript object
        // console.log("Response data:", data);  // Log the data

        return data;  // Return the data so it can be assigned to a variable if needed
    } catch (error) {
        console.error('Error:', error);
    }
}

// Use the async function to get the data
let responseData;
fetchData().then(data => {
    responseData = data;
    const sources = responseData['sources'];
    const filename = '';
    const summary = '';
    for (let i = 0; i < sources.length; i++) {
        const source = sources[i];
        const filename = '###' + sources[i]['filepath'];
        const summary = sources[i]['summary'];
        insertAtLine('ReadMe.md', filename, summary);
    }
    function insertAtLine(filePath, filename, summary){
            fs.readFile(filePath, 'utf8', (err, data) => {
                if (err) {
                return console.error(`Error reading file: ${err.message}`);
                }

                // Split the file content by lines
                let lines = data.split('\n');
                // console.log('lines: ', lines);
                let lastNonEmptyIndex = -1;
                for (let i = lines.length - 1; i >= 0; i--) {
                    if (lines[i].trim() !== '') {
                        lastNonEmptyIndex = i+1;
                        break;
                    }
                }

                if (lastNonEmptyIndex === -1) {
                    return console.error('Could not find the "Code Description" line');
                }

                lines.splice(lastNonEmptyIndex, 0, filename, summary);

                const updatedContent = lines.join('\n');
            
                fs.writeFile(filePath, updatedContent, 'utf8', (err) => {
                    if (err) {
                      return console.error(`Error writing file: ${err.message}`);
                    }
                    console.log('File updated successfully!');
                });
        });
    }
});


    




