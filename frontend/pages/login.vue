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
              prepend-icon="mdi-account"
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
  layout: false,
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login () {
      try {
        const self = this
        const resp = await this.$axios.post('user/login/', {
          username: this.username,
          password: this.password
        })
        self.$auth.setToken('local', 'Bearer ' + resp.data.access)
        self.$auth.setRefreshToken('local', resp.data.refresh)
        self.$axios.setHeader('Authorization', 'Bearer ' + resp.data.access)
        self.$auth.ctx.app.$axios.setHeader('Authorization', 'Bearer ' + resp.data.access)
        self.$axios.get('user/').then((resp) => { self.$auth.setUser(resp.data); self.$router.push('/') })
      } catch (error) {
        if (error) {
          this.$toast.error('Ошибка! Неверное имя пользователя или пароль!')
        }
      }
    }
  }
}
</script>
