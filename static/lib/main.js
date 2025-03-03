let actions = {}
$(document).ready(function () {
    reload_table();

    setInterval(function() {
        reload_table();
    }, 5000);     

    $('#stop_all').on('click', function(event) {
        $.ajax({
            url: '/executor/action',
            type: 'DELETE',
            success: function(result) {
                console.log(result);            
            }
        });
    });

    $('#set_execution_time').on('click', function(event) {
        const execution_time = $('#execution_time').val();
        $.ajax({
            url: '/executor/config/time/' + execution_time,
            type: 'POST',
            success: function(result) {
                console.log(result);            
            }
        });
    });    
});

function reload_table() {
    $.getJSON('/executor/action', function(data) {
        let table_content = [];
        actions = data;                
        $.each(data, function(key, val) {
            table_content.push('<tr id="' + key + '">');
            table_content.push('<td>' + val['name'] + '</td>');
            table_content.push('<td>' + val['description'] + '</td>');
            table_content.push('<td>' + val['executions'].length + '</td>');
            table_content.push('<td>' + val['iopin'] + '</td>'); //GPIO mapping
            if(val['executions'].length > 0) {
                table_content.push('<td> '+ eval_execution_status(val['executions']) +' </td>');    
            } else {
                table_content.push('<td> Finished </td>');
            }

            if(check_if_execution_running(val['executions'])) {
                table_content.push('<td>' + '<button id="trigger_' + key + '" class="w3-btn w3-blue" disabled>Trigger</button>'  + '</td>');
            } else {
                table_content.push('<td>' + '<button id="trigger_' + key + '" class="w3-btn w3-blue">Trigger</button>'  + '</td>');
            }

            table_content.push('<td>' + '<button id="stop_' + key + '" class="w3-btn w3-red">Stop</button>'  + '</td>');
            table_content.push('</tr>');
        });
        
        $('#data_table').html(table_content.join());
        for (i = 0; i < actions.length; i++) {
            $('#trigger_'+i).on('click', function(event) {
                $(this).prop("disabled",true);
                var actionid = Number(event.target.id.slice(-1));
                actionid += 1;
                $.get('/executor/action/' + actionid, function(result) {
                    console.log(result);
                });
            });

            $('#stop_'+i).on('click', function(event) {
                var actionid = Number(event.target.id.slice(-1));
                actionid += 1;
                $.ajax({
                    url: '/executor/action/'+actionid,
                    type: 'DELETE',
                    success: function(result) {
                        console.log(result);            
                    }
                });
            });
        }
    });
}

function check_if_execution_running(executions) {
    if(executions.length === 0) {
        return false;
    }
    var last = executions.at(-1); // get last execution
    if (last['status'] === 'EXECUTING') {
        return true;
    } else {
        return false;
    }
}

function stop_all_actions() {
    $.delete('/executor/action', function(data) {
        // TODO reset trigger buttons
    });
}

function eval_execution_status(executions) {
    var last = executions.at(-1); // get last execution
    if (last['status'] === 'EXECUTING') {     
        return 'EXECUTING ' + last['triggeredAt'];
    } else {
        return 'Finished last at ' + last['finishedAt']
    }          
} 