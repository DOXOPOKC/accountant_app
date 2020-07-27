<template lang="pug">
  v-col(cols="12")
      v-menu(
        ref="actTimeMenu"
        v-model="actTimeMenu"
        :close-on-content-click="false"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      )
        template(v-slot:activator="{ on, attrs }")
          v-text-field(
            v-model="actTime"
            label="Введите время"
            prepend-icon="mdi-clock-outline"
            readonly
            v-bind="attrs"
            v-on="on"
          )
        v-time-picker(
          v-if="actTimeMenu"
          v-model="actTime"
          full-width
          @click:minute="$refs.actTimeMenu.save(actTime)"
        )
</template>

<script>
export default {
  name: '',
  data: () => ({
    actTimeMenu: false
  }),
  computed: {
    actTime: {
      set (actTime) {
        this.$store.commit('act/SET_ACT', { time: actTime })
      },
      get () {
        return this.$store.state.act.detail.time
      }
    }
  }
}
</script>
