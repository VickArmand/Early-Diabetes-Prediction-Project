const table= document.getElementById('reportstable');
const tableBody= table.querySelector('tbody');
var selectedgender=document.getElementById('genderselection');
var selectedoutcome=document.getElementById('outcomeselection');
var parameters
function filterdetails(){
    if (selectedgender.options[selectedgender.selectedIndex].value=='' && selectedoutcome.options[selectedoutcome.selectedIndex].value==''){
        alert('Please select appropiate fields for filtering');
    }
    else if(selectedgender.options[selectedgender.selectedIndex].value=='' && selectedoutcome.options[selectedoutcome.selectedIndex].value!==''){
        parameters='gender';
        var server_data = {
            "Gender": null,
            "Outcome": selectedoutcome.options[selectedoutcome.selectedIndex].value,
        };
            
           const xmlhttp= new XMLHttpRequest();
           xmlhttp.open('POST','/doctors/fetchrecords',true);
           xmlhttp.setRequestHeader('Content-type','application/json; charset=UTF-8')
           xmlhttp.send(JSON.stringify(server_data));
           xmlhttp.onreadystatechange=()=>{
               if(xmlhttp.readyState==4 && xmlhttp.status==200){

                   var users= JSON.parse(xmlhttp.responseText);
                   console.log(users);
                   output='';
                for (var i in users){
                    output+='<tr> '+'<td>'+users[i].id+'</td>'+'<td>'+users[i].name+'</td>'+'</tr>'
                }
                listvalues.innerHTML=output;
               }
            }
    }
    else if(selectedgender.options[selectedgender.selectedIndex].value!=='' && selectedoutcome.options[selectedoutcome.selectedIndex].value==''){
        parameters='outcome';
        var server_data = {
            "Gender": selectedgender.options[selectedgender.selectedIndex].value,
            "Outcome": null,
        };
        console.log(JSON.stringify(server_data))
           const xmlhttp= new XMLHttpRequest();
           xmlhttp.open('POST','/doctors/fetchrecords',true);
           xmlhttp.setRequestHeader('Content-type','application/json; charset=UTF-8')
           xmlhttp.send(JSON.stringify(server_data));
           xmlhttp.onreadystatechange=()=>{
               if(xmlhttp.readyState==4 && xmlhttp.status==200){

                   var users= JSON.parse(xmlhttp.responseText);
                   console.log(users);
                   output='';
                for (var i in users){
                    output+='<tr> '+'<td>'+users[i].id+'</td>'+'<td>'+users[i].name+'</td>'+'</tr>'
                }
                listvalues.innerHTML=output;
               }
            }
    }
    else{
        var server_data = {
            "Gender": selectedgender.options[selectedgender.selectedIndex].value,
            "Outcome": selectedoutcome.options[selectedoutcome.selectedIndex].value,
        };
        console.log(JSON.stringify(server_data))
        const xmlhttp= new XMLHttpRequest();
        xmlhttp.open("POST","/doctors/fetchrecords",true);
        xmlhttp.setRequestHeader('Content-type','application/json; charset=UTF-8')
        xmlhttp.send(JSON.stringify(server_data));
        xmlhttp.onreadystatechange=()=>{
            if(xmlhttp.readyState==4 && xmlhttp.status==200){
                var users= JSON.parse(xmlhttp.responseText);
                console.log(users);
                output='';
                for (var i in users){
                    output+='<tr> '+'<td>'+users[i].id+'</td>'+'<td>'+users[i].name+'</td>'+'</tr>'
                }
                listvalues.innerHTML=output;
            }
        }
            }
        }