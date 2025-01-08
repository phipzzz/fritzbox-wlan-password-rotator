setTimeout(() => {
    window.location.reload();
}, 2 * 60 * 1000);

function confirmUpdatePassword(event) {
    const userConfirmed = confirm(
        "Generating a new password will cut off all existing connections. Are you sure?"
    );
    if (!userConfirmed) {
        event.preventDefault();
    }
}
