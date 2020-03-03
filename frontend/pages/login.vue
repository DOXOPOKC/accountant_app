<template>
  <v-row
    align="center"
    justify="center"
  >
    <v-col
      cols="12"
      sm="8"
      md="4"
    >
      <v-form ref="form" @submit.prevent="login">
        <v-card class="elevation-12">
          <v-toolbar
            color="primary"
            dark
            flat
          >
            <v-spacer />
            <v-toolbar-title>Sign in</v-toolbar-title>
            <div class="flex-grow-1" />
          </v-toolbar>
          <v-card-text>
            <v-text-field
              v-model="username"
              label="Login"
              name="login"
              prepend-icon="mdi-person"
              type="text"
            />

            <v-text-field
              id="password"
              v-model="password"
              label="Password"
              name="password"
              prepend-icon="mdi-lock"
              type="password"
            />
          </v-card-text>
          <v-card-actions>
            <div class="flex-grow-1" />
            <v-btn type="submit" color="primary">
              Login
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    // ...mapActions(['users/']),
    login () {
      // this.error = null
      // return this.$auth
      //   .loginWith('local', {
      //     data: {
      //       username: this.username,
      //       password: this.password
      //     }
      //   })
      //   .catch((e) => {
      //     this.error = e + ''
      //   })
      const self = this
      this.$axios.post('/user/login/', {
        username: this.username,
        password: this.password
      }).then(function (resp) {
        self.$auth.setToken('local', 'Bearer ' + resp.data.access)
        self.$auth.setRefreshToken('local', resp.data.refresh)
        self.$axios.setHeader('Authorization', 'Bearer ' + resp.data.access)
        self.$auth.ctx.app.$axios.setHeader('Authorization', 'Bearer ' + resp.data.access)
        self.$axios.get('/contragents/').then((resp) => { self.$router.push('/') })
      }).catch((err) => {
        if (err.response) {
          self.usernameErrors = []
          self.passwordErrors = []
          const status = err.response.data.detail.status
          if (status === 404) { self.usernameErrors = ['That user does not exist'] } else if (status === 401) { self.passwordErrors = ['Invalid password'] }
        }
      })
    }
  }
}
</script>
