//Datadogのユーザーリスト作成
function ddUserList(){
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  let env =["micinjp","iriko","sandbox","sui","miroha","psp-followup","videocall"];
  for(let datadog_env = 0; datadog_env < env.length; datadog_env++){ 
   let ddSheet = ss.getSheetByName(env[datadog_env]+"_datadog");
   ddSheet.clear();
   let k=1;
   let ddCells = [];
   let ddUsers = DatadogAPI_GET(env[datadog_env]);
   ddCells.push(["type","id","name","handle","e-mail","status","roles","roles2"]);
   for(let i = 0; i < ddUsers.data.length; i++){   
    if(ddUsers.data[i].attributes.status != "Disabled"){
     let row = [];
     row.push(ddUsers.data[i].type);
     row.push(ddUsers.data[i].id) 
     row.push(ddUsers.data[i].attributes.name);
     row.push(ddUsers.data[i].attributes.handle);
     row.push(ddUsers.data[i].attributes.email);
     row.push(ddUsers.data[i].attributes.status);
     ddCells.push(row)

     let row_roles =[];
     for(let j = 0; j < ddUsers.data[i].relationships.roles.data.length;j++){
     row_roles.push(ddUsers.data[i].relationships.roles.data[j].id);
     let ddRoles = DatadogAPI_GET_roles(env[datadog_env],row_roles[j]);
     row.push(ddRoles.data.attributes.name);
     }
    //代替求む,roleを複数表示することで配列の大きさがバラバラになってしまうことで出力に難あり
    let flag = 0;
    while(flag == 0){
   　 if(ddCells[k].length <= 7){
       ddCells[k]=ddCells[k].concat([""]);
      }
    if(ddCells[k].length == 8){
          flag = 1;
     }     
    }
      k++;
   }
  }
  ddSheet.getRange(1,1,ddCells.length,8).setValues(ddCells);
   // DdSheet.getRange(1,1,DdCells.length,row.length).setValues(DdCells);
  Logger.log(env[datadog_env]+'-Datadogのユーザリストを作成しました。');
 }
}

function DatadogAPI_GET(env){
  var url = "https://api.datadoghq.com/api/v2/users";
  //DD-API-KEY,DD-APPLICATION-KEY共にdatadogのシートの特徴名を-で繋げば使える
  const API_KEY = PropertiesService.getScriptProperties().getProperty("DD-API-KEY-"+env);
  const APP_KEY = PropertiesService.getScriptProperties().getProperty("DD-APPLICATION-KEY-"+env);
  var headers = {
    'DD-API-KEY':API_KEY,
    'DD-APPLICATION-KEY':APP_KEY,
    "Accept": "application/json",
    "Content-type": "application/json"
  }

  var options = {
    "method" : "get",
    "headers" : headers,
  };
  var res = UrlFetchApp.fetch(url + "?page[size]=50&page[number]=0&sort=name&sort_dir=desc", options);
  // Logger.log(JSON.parse(res.getContentText()));
  // Logger.log(res)
  //return  UrlFetchApp.fetch(url, options);
  let json =  UrlFetchApp.fetch(url, options);
  return JSON.parse(res.getContentText());
  // Logger.log(json);
  // return json;
}

function DatadogAPI_GET_roles(env,role_id){
  var url = "https://api.datadoghq.com/api/v2/roles/";
 // PropertiesService.getScriptProperties().setProperty('DD-API-KEY-sui',''); //DD-API-KEY,DD-APPLICATION-KEY共にdatadogのシートの特徴名を-で繋げば使える
  const API_KEY = PropertiesService.getScriptProperties().getProperty("DD-API-KEY-"+env);

 // PropertiesService.getScriptProperties().setProperty('DD-APPLICATION-KEY-sui','');
  const APP_KEY = PropertiesService.getScriptProperties().getProperty("DD-APPLICATION-KEY-"+env);


  var headers = {
    'DD-API-KEY':API_KEY,
    'DD-APPLICATION-KEY':APP_KEY,
    "Accept": "application/json",
    "Content-type": "application/json"
  }

  var options = {
    "method" : "get",
    "headers" : headers,
  };
  var res = UrlFetchApp.fetch(url + role_id,options);
  // var res = UrlFetchApp.fetch(url +"role_id", options);
  // Logger.log(JSON.parse(res.getContentText()));
  // Logger.log(res)
  //return  UrlFetchApp.fetch(url, options);
  let json =  UrlFetchApp.fetch(url, options);
  return JSON.parse(res.getContentText());
  // Logger.log(json);
  // return json;
}

