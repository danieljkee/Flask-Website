// this function is going to take the note id that
// we passed and it is going to send a post request
// to delete note endpoint
// after we get a response from the delete note endpoint
// it is going to refresh the page
function deleteNote(noteId) {
  // sending to endpoint /delete-note
  fetch("/delete-note", {
    // defining HTTP method to server
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}