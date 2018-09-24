// Convert to local tz
function toLocal(dt) {
    dt = new Date(dt);
    return dt.toISOString();
}

// Update an object's value to tz
function updateTimeValue(id, dt) {
    $(id).text(toLocal(dt));
    $(id).attr("datetime", dt);
}