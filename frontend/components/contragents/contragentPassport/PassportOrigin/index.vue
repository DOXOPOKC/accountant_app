<template lang="pug">
  v-col(cols="2")
    v-text-field(
      dense
      v-model="opf"
      label="Кем выдан паспорт"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    opf: {
      set (opf) {
        this.$store.commit('contragents/SET_CONTRAGENT', { opf })
      },
      get () {
        return this.$store.state.contragents.detail.opf
      }
    }
  }
}
</script>
