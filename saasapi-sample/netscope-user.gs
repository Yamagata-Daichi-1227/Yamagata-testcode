//Netskopeのユーザーリスト作成
function nsUserList(){
  ss = SpreadsheetApp.getActiveSpreadsheet();
  nsSheet = ss.getSheetByName("Netskope");
  nsSheet.clear();

  nsCells.push(["email", "active", "givenName", "familyName", "id"]);
  nsUsers = netskopeAPI_GET("Users");
    for(let i = 0; i < nsUsers.Resources.length; i++){
      var row = [];
      row.push(nsUsers.Resources[i].emails[0].value);
      row.push(nsUsers.Resources[i].active)
      row.push(nsUsers.Resources[i].name.givenName);
      row.push(nsUsers.Resources[i].name.familyName);
      row.push(nsUsers.Resources[i].id);

      nsCells.push(row);
    }
    nsSheet.getRange(1,1,nsCells.length,5).setValues(nsCells);
    Logger.log('Netskopeユーザリストを作成しました。');
}

function getUserGroups(){
  ss = SpreadsheetApp.getActiveSpreadsheet();
  let nsGroupSheet = ss.getSheetByName("Netskope_Group");

  const groups = netskopeAPI_GET("Groups");

  for(let i = 0; i < groups.Resources.length; i++){
    let g = groups.Resources[i];
    let cells = [];
    Logger.log(g);
    cells.push([g.displayName]);
    g.members.forEach(m => {
      cells.push([m]);
    })
    nsGroupSheet.getRange(1,1,1,cells[0].length).setValues(cells);
  }
}

function formatGroupList(){
  const transpose = a => a[0].map((_, c) => a.map(r => r[c]));
  ss = SpreadsheetApp.getActiveSpreadsheet();
  let groupSheet = ss.getSheetByName("Netskope_Group");
  let groupList = groupSheet.getRange(1,1,groupSheet.getLastRow()-1,groupSheet.getLastColumn()).getValues();
  // groupSheet.clear()
  // Logger.log("no")
  cells = [];
  groupList = transpose(groupList);
  Logger.log(groupList)
  for(let i = 0; i < groupList.length; i++){
    let groupMembers = [groupList[i][0]];
    groupList[i].forEach(tmpData => {
      if(tmpData.indexOf("@") != -1){
        groupMembers.push(tmpData)
      }
    groupMembers = transpose([groupMembers]);
    })
    groupSheet.getRange(1,i,groupMembers[0].length,1).setValues(groupMembers);
  }
}

function add_members_toGroup(){
  let nsuser_id = "";
  ss = SpreadsheetApp.getActiveSpreadsheet();
  accSheet = ss.getSheetByName("統合マスタ");
  let accList = accSheet.getRange(2,1,accSheet.getLastRow() - 1,accSheet.getLastColumn()).getValues();
  const engGroupID = "";
  const micinExpEngGroupID = "";
  const externalGroupID = "";
  for(let i = 0; i < accList.length; i++){
    nsuser_id = accList[i][15];
    if(nsuser_id !== ""){
      if(accList[i][6].indexOf("Engineer") != -1){
        //Engineerのユーザー
        netskopeAPI_PATCH("Groups/" + engGroupID, nsuser_id);
      }else if((accList[i][4] == "MICIN_Employee") || (accList[i][4] == "MICIN_Intern")){
        //EngineerじゃないMICINユーザー
        netskopeAPI_PATCH("Groups/" + micinExpEngGroupID, nsuser_id);
      }
      if((accList[i][4] != "MICIN_Employee") && (accList[i][4] != "MICIN_Intern")){
        //社外のユーザー
        netskopeAPI_PATCH("Groups/" + externalGroupID, nsuser_id)
      }
    }
  }
}

function netskopeAPI_POST(method, data){
  var url = "https://addon-micin2.goskope.com/SCIM/V2/d3mqCz1vyzg5A8R9zoiQ/" + method;
  const accessToken = PropertiesService.getScriptProperties().getProperty("NETSKOPE_ACCESS_TOKEN");

  var headers = {
    "Authorization": "Bearer "+ accessToken,
    "Accept": "application/json",
    "Content-type": "application/json"
  }

  var options = {
    "method" : "post",
    "headers" : headers,
    "payload" : JSON.stringify(data)
  };

  return UrlFetchApp.fetch(url, options);
}