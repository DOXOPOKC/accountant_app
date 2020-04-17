<template lang="pug">
    v-chip(
      outlined
      :color="is_func ? 'primary' : 'error'"
    )
      span {{ getIsFuncText }}
</template>

<script>
export default {
  data: () => ({
    // statusList: [
    //   { text: 'Активен', value: true },
    //   { text: 'Неактивен', value: false }
    // ]
  }),
  computed: {
    getIsFuncText () {
      // Object.keys(object).find(key => object[key] === value)
      return this.is_func ? 'Активен' : 'Неактивен'
    },
    is_func: {
      set (isFunc) {
        this.$store.commit('contragents/SET_CONTRAGENT', { is_func: isFunc })
      },
      get () {
        return this.$store.state.contragents.detail.is_func
      }
    }
  }
}
// disabled  ? 'Активен': 'Неактивен'
</script>
