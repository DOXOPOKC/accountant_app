export const routeOption = (route, key, value) => {
  console.log(route)
  console.log(key, value)
  return route.matched.some((m) => {
    if (process.client) {
      // Client
      console.log(m)
      return Object.values(m.components).some(
        component => component.options && component.options[key] === value
      )
    } else {
      // SSR
      return Object.values(m.components).some(component =>
        Object.values(component._Ctor).some(
          ctor => ctor.options && ctor.options[key] === value
        )
      )
    }
  })
}

export function normalizePath (path = '') {
  // Remove query string
  let result = path.split('?')[0]

  // Remove redundant / from the end of path
  if (result.charAt(result.length - 1) === '/') {
    result = result.slice(0, -1)
  }

  return result
}

export default function (ctx) {
  const { login, callback } = ctx.$auth.options.redirect
  console.log(ctx.$auth)
  // const pageIsInGuestMode = routeOption(ctx.route, 'auth', 'guest')
  const insidePage = page => normalizePath(ctx.route.path) === normalizePath(page)

  if (ctx.$auth.$state.loggedIn) {
    // -- Authorized --
    if (!login || insidePage(login)) {
      ctx.$auth.redirect('home')
    }
  } else if (!callback || !insidePage(callback)) {
    ctx.$auth.redirect('login')
  }
}
