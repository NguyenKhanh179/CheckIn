let loader = document.getElementById("loader_container");
let content = document.getElementById("content_container");
let content_department = document.getElementById("c_list_departments");
let content_container_body = document.getElementById("content_container_body");

let list_department=[];
let report=[];


function today(){
    var d = new Date();
    var curr_date = d.getDate();
    var curr_month = d.getMonth() + 1;
    var curr_year = d.getFullYear();
    if(curr_date<10) 
    {
        curr_date='0'+curr_date;
    } 

    if(curr_month<10) 
    {
        curr_month='0'+curr_month;
    } 
    return (curr_year + "-" + curr_month + "-" + curr_date);
}
let report_date_param = document.getElementById("report_date_param");
report_date_param.value= today();

load_content = () => {
    show_loading();
    fetch(
      "/api/v1/dailyreportapi/getDailyReport?report_date="+report_date_param.value,
    ).then(res => {
        return res.json();
    })
    .then(data => {
//        list_department= [{"id": "all", "name": "All"}];
        list_department= [];
        data.departments.forEach( (dp)=> {
            list_department.push(dp);
        });
        report= data.report;
        load_list_department();
        // select first item
//        if(list_department && list_department[0] && list_department[0].id){
//            loadDepartmentReport(list_department[0].id);
//        }
        hidden_loading();
    }).catch(err => {
        console.error(err);
    });

    
};

show_loading = () => {
    content.classList.add("hidden");
    loader.classList.remove("hidden");
};
hidden_loading = () => {
    content.classList.remove("hidden");
    loader.classList.add("hidden");
};


const department_list_table_template = `
<div class="list-group" id="list-department-tab" role="tablist">
    {LIST_DEPARTMENTS}
</div>
`
;
const department_list_row_tempalte = `
<a class="list-group-item list-group-item-action link" id="{DEPARTMENT_ID}"
style="" href="#{DEPARTMENT_ID}"
onclick="loadDepartmentReport('{DEPARTMENT_ID}')">
{DEPARTMENT_NAME}
</a>
`
;
load_list_department = () => {
    let list_department_html = "";
    list_department.forEach(
        (department) => {
            let td_html = department_list_row_tempalte;
            td_html = td_html.replace("{DEPARTMENT_ID}", department.id)
            .replace("{DEPARTMENT_ID}", department.id).replace("{DEPARTMENT_ID}", department.id);
            td_html = td_html.replace("{DEPARTMENT_NAME}", department.name);
            list_department_html = list_department_html + td_html;
        }
    );
    content_department_html = department_list_table_template.replace("{LIST_DEPARTMENTS}", list_department_html);
    content_department.innerHTML = content_department_html;
}
;


loadDepartmentReport = (id) => {
    console.log("run " + id);     
    activeDepartmentItem(id);
    loadReport(id);
};

activeDepartmentItem= (id) => {
    let list_department_element=document.getElementById("list-department-tab");
    let current_select_element = list_department_element.getElementsByClassName("active");
    let select_element = document.getElementById(id);
    if (current_select_element && current_select_element[0]) {
        current_select_element[0].className = current_select_element[0].className.replace(" active", "");
    }
    if (select_element) {
        select_element.className += " active";
    }
    ;
}

const report_department_tr_template = `
    <tr>
        <th scope="row">
            <div class="btn-group btn-group-xs" style="display: flex;">
                <a href="/mbcheckin/show/{id}" class="btn btn-sm btn-default" data-toggle="tooltip" rel="tooltip" title="" data-original-title="Show record">
                    <i class="fa fa-search"></i>
                </a>
                <a href="/mbcheckin/edit/{id}" class="btn btn-sm btn-default" data-toggle="tooltip" rel="tooltip" title="" data-original-title="Edit record">
                    <i class="fa fa-edit"></i>
                </a>
            </div>
        </th>
        <td>{username}</td>
        <td>{phong}</td>
        <td>{checkin}</td>
        <td>{auth_user}</td>
        <td>{reason}</td>

    </tr>
`
;
loadReport = (department_id) => {
    let report_html = "";
    report.forEach(
        (check_in_log) => {
            if(department_id && (check_in_log.phong == department_id || department_id=="all")){
                let row = report_department_tr_template;
                row = row.replace("{id}", check_in_log.id).replace("{id}", check_in_log.id);
                row = row.replace("{username}", check_in_log.username);
                row = row.replace("{phong}", check_in_log.phong);
                row = row.replace("{checkin}", check_in_log.checkin);
                row = row.replace("{reason}", check_in_log.reason);
                row = row.replace("{auth_user}", check_in_log.auth_user);
                report_html = report_html + row;
            }            
        }
    );
    if(report_html){
        content_container_body.innerHTML = report_html;
    }else{
        content_container_body.innerHTML = "<tr><td>No Data</td></tr>";
    }
    
};


load_content();