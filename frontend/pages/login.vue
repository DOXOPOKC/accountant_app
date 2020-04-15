<template lang="pug">
  v-row(
    align="center"
    justify="center"
  )
    v-col(
      cols="12"
      sm="8"
      md="4"
    )
      validation-observer(slim v-slot="{ handleSubmit}")
        v-form(ref="form" @submit.prevent="handleSubmit(login)")
          v-card(class="elevation-12")
            v-toolbar(
              color="primary"
              dark
              flat
            )
              v-spacer
              v-toolbar-title Sign in
              v-spacer
            v-card-text
              validation-provider(rules="required" v-slot="{ errors }")
                v-text-field(
                  v-model="username"
                  label="Login"
                  name="login"
                  prepend-icon="mdi-account"
                  type="text"
                  :error-messages="errors"
                )
              validation-provider(rules="required" v-slot="{ errors }")
                v-text-field(
                  id="password"
                  v-model="password"
                  label="Password"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                  :error-messages="errors"
                )
            v-card-actions
              v-spacer
              v-btn(type="submit" color="primary")
                | Login
</template>

<script>
import { ValidationObserver, ValidationProvider } from 'vee-validate'

export default {
  components: {
    ValidationObserver,
    ValidationProvider
  },
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
        const { access, refresh } = resp.data
        self.$auth.setToken('local', 'Bearer ' + access)
        self.$auth.setRefreshToken('local', refresh)
        self.$axios.setHeader('Authorization', 'Bearer ' + access)
        // self.$auth.ctx.app.$axios.setHeader('Authorization', 'Bearer ' + access)
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
