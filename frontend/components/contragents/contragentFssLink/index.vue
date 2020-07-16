<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      v-model="fssLink"
      label="Ссылка на сайт фсс"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    fssLink: {
      set (fssLink) {
        this.$store.commit('contragents/SET_CONTRAGENT', { fss_link: fssLink })
      },
      get () {
        return this.$store.state.contragents.detail.fss_link
      }
    }
  }
}
</script>
