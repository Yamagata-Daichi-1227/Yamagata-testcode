function boxUserList() {
  //作業対象シートオブジェクトの取得
  ss = SpreadsheetApp.getActiveSpreadsheet();
  boxSheet = ss.getSheetByName("Box");
  //シート初期化
  
  boxUsers = boxAPI_GET();

  //データがうまく取得できたら
  if (boxUsers) {
    boxCells.push(["type","id","name","login","created_at","modified_at","status","jobtitle"]);

    for(let i = 0; i < boxUsers.entries.length; i++){
      let row = [];
      row.push(boxUsers.entries[i].type);
      row.push(boxUsers.entries[i].id);
      row.push(boxUsers.entries[i].name);
      row.push(boxUsers.entries[i].login);
      row.push(boxUsers.entries[i].created_at);
      row.push(boxUsers.entries[i].modified_at);
      row.push(boxUsers.entries[i].status);
      row.push(boxUsers.entries[i].jobtitle);
      boxCells.push(row);
    }
    boxSheet.clear();
    boxSheet.getRange(1,1,boxCells.length,boxCells[0].length).setValues(boxCells);
  }


}

function getBoxToken(){
  const url = 'https://api.box.com/oauth2/token';

  // const box_client_id = PropertiesService.getScriptProperties().getProperty("BOX_CLIENT_ID");
  // const box_client_secret = PropertiesService.getScriptProperties().getProperty("BOX_CLIENT_SECRET");
  
  const headers = {
    'Content-Type' : 'application/x-www-form-urlencoded',
  };
  
  const refresh_token =

  let data = {
    'grant_type' : 'refresh_token',
    'client_id' : box_client_id,
    'client_secret' : box_client_secret,
    'refresh_token' : refresh_token
  };
  
  let options = {
    'method': 'POST',
    'headers': headers,
    'payload': data,
    muteHttpExceptions: true,
  };

  const response = UrlFetchApp.fetch(url, options);
  const tmpTokenObjJSON = JSON.parse(response);
  // Logger.log(tmpTokenObjJSON)
  // Logger.log(tmpTokenObjJSON["access_token"]);
  // Logger.log(tmpTokenObjJSON["refresh_token"]);
  PropertiesService.getScriptProperties().setProperty("BOX_REFRESH_TOKEN",tmpTokenObjJSON["refresh_token"]);
  return tmpTokenObjJSON["access_token"];
}

function boxAPI_GET(){
  const api_box_com = "api.box.com"
  let url = "https://" + api_box_com + "/2.0/";
  const accessToken = getBoxToken();

  var headers = {
    "Authorization": "Bearer "+ accessToken,
    "Accept": "application/json",
    "Content-type": "application/json",
  }

  var options = {
    "method": "get",
    "headers": headers
  };

  var res = UrlFetchApp.fetch(url + "users", options);
  // Logger.log(JSON.parse(res.getContentText()));
  // Logger.log(res)
  return JSON.parse(res.getContentText());
}