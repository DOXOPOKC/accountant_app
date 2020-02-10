<template lang="pug">
  v-row(
    class="fill-height"
    justify="center"
    align="start"
    no-gutters
  )
    v-col(
      xs12
      sm8
      md6
    )
      v-card(
        flat
        exact
      )
        v-card-title(class="headline font-weight-light px-10")
          | Пакет № {{ package.id }}
        v-card-text
          | {{package}}
</template>

<script>
import { mapState } from 'vuex'
import { ValidationProvider, ValidationObserver } from 'vee-validate'
import { types } from '~/store/packages'

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  async asyncData ({ $axios, store, params }) {
    console.log(params)
    await store.dispatch(`packages/${types.FETCH_PACKAGE}`, { contragentId: params.contragentId, packageId: params.id })
  },
  data: () => ({}),
  computed: {
    ...mapState({
      package: state => state.packages.detail
    }),
    panels () {
      return [...Array(this.contragentInfo.length).keys()]
    }
  },
  methods: {}
}
</script>
