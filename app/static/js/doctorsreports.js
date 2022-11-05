const table= document.getElementById('reportstable');
// const tableBody= table.querySelector('tbody');
const tableBody= document.querySelector('#tbody2');
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
                   output='<tr> ';
                for (var i in users.rows){
                   for(num=0;num<6;num++){
                    output+='<td>'+users.rows[i][num]+'</td>'+'<td>'+users.rows[i][num]+'</td>'
                 }
                }
                output+='</tr>'
                console.log(output)
                tableBody.innerHTML=output;
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
             for (var i in users.rows){
                output+='<tr class="bg-white border-b  dark:border-gray-700">'
                 for(num=0;num<6;num++){
                    output+='<td class="py-2 px-2">'+users.rows[i][num]+'</td>'
                 }
                 output+='</tr>'
             }
             tableBody.innerHTML=output
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
             for (var i in users.rows){
                output+='<tr class="bg-white border-b  dark:border-gray-700">'
                 for(num=0;num<6;num++){
                    output+='<td class="py-2 px-2">'+users.rows[i][num]+'</td>'
                 }
                 output+='</tr>'
             }
             tableBody.innerHTML=output
            }
        }
            }
        }
const list_source=document.querySelector('tbody');
let list_items= new Array();
let cell=[]
// list_source.childNodes.forEach((x,y)=>{
//     console.log(x.innerHTML,y)
// })
const list_source_row=list_source.getElementsByTagName('tr');
console.log(list_source.children.length)
console.log(list_source_row[0].children.length)
// list_source.querySelector('tr').childNodes.forEach((x,y)=>{
//     console.log(x.innerHTML,y)
// })
for (let row=0;row<list_source.children.length;row++){
    list_items=[]
    //for (let col=0;col<list_source_row[row].children.length;col++){
    //console.log(row, col);
    console.log(row);
    cell.push([list_source_row[row].innerText]);
    // console.log(list_source_row[row].innerText);
    list_items[row]=cell;
    console.log(cell); 
    //}
}

console.log(list_items);

        // const list_items= [
        //     "Item 1",
        //     "Item 2",
        //     "Item 3",
        //     "Item 4",
        //     "Item 5",
        //     "Item 6",
        //     "Item 7",
        //     "Item 8",
        //     "Item 9",
        //     "Item 10",
        //     "Item 11",
        //     "Item 12",
        //     "Item 13",
        //     "Item 14",
        //     "Item 15",
        //     "Item 16",
        //     "Item 17",
        //     "Item 18",
        //     "Item 19",
        //     "Item 20",
        //     "Item 21",
        //     "Item 22",
        //     "Item 23",
        //     "Item 24",
        // ];
const listElement= document.getElementById('tbody2');
const paginationElement=document.getElementById('pagination');
// const paginationElement=document.getElementsByTagName('tr');
let currentPage=1;
let rows=5;
function displayList(items,wrapper,rows_per_page,page){
    wrapper.innerHTML="";
    page--;
    let start=rows_per_page* page;
    let end=start+ rows_per_page;
    console.log(start,end);
    for (let row=0;row<items.length;row++){
        //for (let col=0;col<list_source_row[row].children.length;col++){
        //console.log(row, col);
        console.log(items);
        cell.push([items[row].innerText]);
        // console.log(list_source_row[row].innerText);
        items[row]=cell;
        console.log(cell); 
        //}
    }
    let paginatedItems=items.slice(start,end);

    // The slice() method slices out a piece of an array into a new array.
    // The slice() method can take two arguments like slice(1, 3).
    // The method then selects elements from the start argument, and up to (but not including) the end argument.
    console.log(paginatedItems);
    let output=''
    output+='<tr class="bg-white border-b  dark:border-gray-700">'
    for (let i=0;i<paginatedItems.length; i++)
    {
        output+='<td class="py-2 px-2">'+ +'</td>'
        // let item=paginatedItems[i];
        // let itemElement=document.createElement('tr');
        // itemElement.classList.add('item');
        // itemElement.innerText=item;
        // wrapper.appendChild(itemElement);
    }
    output+='</tr>'
    SetupPagination(items,paginationElement,rows_per_page)

}
function SetupPagination(items,wrapper,rows_per_page){
    wrapper.innerHTML="";
    let page_count=Math.ceil(items.length/rows_per_page);
    for(let i=1;i<page_count+1;i++){
        let btn=PaginationButton(i,items);
        wrapper.appendChild(btn);
    }
}
function PaginationButton(page,items){
    let button= document.createElement('button');
    button.innerText=page;
    if(currentPage==page) button.classList.add('active');
    button.addEventListener('click',function(){
        currentPage=page;
        displayList(items,listElement,rows,currentPage);
        // let currentButton=document.querySelector('.pagenumbers button.active');
        // currentButton.classList.remove('active');
        button.classList.add('active');
    })
    return button;
}
displayList(list_items,listElement,rows,currentPage)