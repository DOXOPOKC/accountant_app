<template lang="pug">
  v-col(cols="4")
    v-menu(
      ref="passportDateMenu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="passportDate"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        v-text-field(
          dense
          v-model="passportDate"
          label="Дата выдачи паспорта"
          readonly
          v-on="on"
        )
      v-date-picker(v-model="passportDate" no-title scrollable)
        v-spacer
        v-btn(text color="primary" @click="menu = false") Отмена
        v-btn(text color="primary" @click="$refs.passportDateMenu.save(passportDate)") OK
</template>

<script>
export default {
  data: () => ({
    menu: false
  }),
  computed: {
    passportDate: {
      set (passportDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { passport_date: passportDate })
      },
      get () {
        return this.$store.state.contragents.detail.passport_date
      }
    }
  }
}
</script>
