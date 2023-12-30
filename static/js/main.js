import { Hanko, register } from "https://esm.run/@teamhanko/hanko-elements";

const hankoApi = "https://42bd9cc0-a654-4ac6-be87-ec191b397dba.hanko.io"

const { hanko } = await register(hankoApi)
const hankoClass = new Hanko(hankoApi);


hanko.onAuthFlowCompleted(async () => {
  const { id, email } = await hanko?.user?.getCurrent();

  const response = await fetch(CREATE_USER_ENDPOINT, {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ userId: id, email })
  });

  document.location.href = `${COMPLETE_PROFILE_ENDPOINT}/${id}/`
});

document.getElementById("logout-btn")
  .addEventListener("click", (e) => {
    e.preventDefault();
    hanko.user.logout();
});

hanko.onUserLoggedOut(() => {
  document.location.href = "/"
})

