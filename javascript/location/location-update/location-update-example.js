
var querystring = require('querystring');

const authOptions = {
    username: "",
    password: "",
};

const globalOptions = {
    host: "10.0.0.8",
    port: 8080
};

//use https in live environments
const httpObj = require('http'); 

/**
 * Function to get an access token
 * @param {*} authOptions 
 */
function getTokenRequest(authOptions){

    return new Promise((resolve, reject)=>{

        const data = JSON.stringify(authOptions);

        const req = httpObj.request({
            host: globalOptions.host,
            port: globalOptions.port,
            path: "/rest/authentication/j",
            method: "POST",
            headers: {
                'Content-Type':'application/json',
                'Content-Length':data.length,
            },
        }, (res)=>{

            let responseBody = '';

            console.log(`API HTTP Auth Token Request Status: ${res.statusCode}`);

            res.on('data', (recvData)=>{
                responseBody = responseBody + recvData.toString();
            });

            res.on('end', ()=>{
                resolve(responseBody);
            });

            res.on('error', (error)=>{
                console.log(error);
                reject(error);
            });
        });

        req.write(data);
        req.end();
    });
}
/**
 * Update the location API with fake data
 * @param {*} accessToken 
 */
function updateAPI(accessToken){

    const locationReport = {
        tagId: 20002,
        x: 2,
        y: 2,
        z: 2,
        timestamp: Date.now(),
    };

    console.log("running API request");

    const data = JSON.stringify(locationReport);

    const options = {
        host: globalOptions.host,
        port: globalOptions.port,
        path: "/rest/locationtagupdate/update",
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length':data.length,
            'Authorization': "Bearer " + accessToken,
        }
    };

    const req = httpObj.request(options, (res)=>{

        console.log(`API HTTP Location Update Status: ${res.statusCode}`);

        res.on('data', (recvData)=>{
            process.stdout.write(recvData);
        });

        res.on('error', (error)=>{
            console.error(error);
        });
    });

    req.on('error', (error)=>{
        console.error(error);
    });

    req.write(data);
    req.end();

}

async function doMain(){

    try {
        const token = await getTokenRequest(authOptions);
        console.log(token);

        setInterval(()=> {updateAPI(token)}, 5000);

    }catch(err){
        console.error("Could not get token:" + err);
    }

}

process.on('SIGINT', ()=>{
    console.log("Exiting...");
    process.exit();
});

doMain();




