<template lang="pug">
  v-col(cols="4")
    v-text-field(
      dense
      v-model="passportOrigin"
      label="Кем выдан паспорт"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    passportOrigin: {
      set (passportOrigin) {
        this.$store.commit('contragents/SET_CONTRAGENT', { passport_origin: passportOrigin })
      },
      get () {
        return this.$store.state.contragents.detail.passport_origin
      }
    }
  }
}
</script>
