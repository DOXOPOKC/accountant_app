export default function ({ store, redirect }) {
	if (store.state.auth.loggedIn) {
    console.log(123)
		return redirect('/')
	}
}