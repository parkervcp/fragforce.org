// Convert to local tz
function toLocal(dt) {
    dt = new Date(dt);
    return dt.toLocaleString() + "(" + dt.timezoneOffset + ")";
}

// Update an object's value to tz
function updateTimeValue(id, dt) {
    $(id).text(toLocal(dt));
    $(id).attr("datetime", dt);
}