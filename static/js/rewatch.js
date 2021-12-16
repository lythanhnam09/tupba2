$(function() {
    setTimeout(updateTaskList, 1000);
});

async function updateTaskList() {
    let data = await getData(`http://${getBaseUrl()}/api/task`);
    let tasklistHtml = ''
    if (data.count == 0) {
        tasklistHtml = '<span class="dropdown-label text-center">No task</span>';
    } else {
        for (let task of data.tasks) {
            let taskDone = (task.count - task.left)
            let taskPercent = taskDone / task.count * 100
            tasklistHtml += `
            <span class="dropdown-item">
                <div class="dropdown-label">${task.name} (${taskDone}/${task.count})</div>
                <div class="progress-bar">
                    <div class="value" style="width:${taskPercent}%"></div>
                </div>
            </span>
            `;
        }
    }
    $('#task-list').html(tasklistHtml);
    setTimeout(updateTaskList, 1000);
}