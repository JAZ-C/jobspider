const got = require('got');
module.exports = async () => {
  const res = await got('http://127.0.0.1:8000/?types=0&count=1&protocol=1')
  // const res = await got('http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=100&pro=&city=&port=1&format=json&ss=5&css=&ipport=1&dt=1&specialTxt=3&specialJson=')
  const [[ip, port]] = JSON.parse(res.body);
  console.log(`${ip}:${port}`)
  return `http://${ip}:${port}`
  // return "http://196.192.179.130:59703"
  // console.log(res.body);
  // console.log(JSON.parse(res.body).data[0].IP);
  // return `http://${JSON.parse(res.body).data[0].IP}`
}