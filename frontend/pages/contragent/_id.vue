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
          | Контрагент № {{ contragent.id }}
          v-spacer
          v-btn(
            outlined
            class="text-capitalize"
            color="primary"
            :to="'/contragent/' + $route.params.id + '/packages/'"
          ) Посмотреть пакеты
        v-card-text
          ValidationObserver(
            ref="form"
            v-slot="{ passes }"
          )
            form(@submit.prevent="passes(onSubmit)")
              v-expansion-panels(
                :value="panels"
                accordion
                multiple
                hover
                flat
                tile
              )
                v-expansion-panel(
                  v-for="(item, i) in contragentInfo"
                  :key="i"
                )
                  v-expansion-panel-header {{ Object.keys(item)[0] }}
                  v-expansion-panel-content
                    ValidationProvider(
                      rules="required"
                      v-slot="{ errors }"
                    )
                      v-text-field(
                        v-model="contragent[item]"
                        :label="Object.values(item)[0]"
                        :error-messages="errors"
                      )
        v-card-actions(class="px-10 py-6")
          v-btn(
            color="primary"
            @click=""
            to="put /contragents/{id}/packages/{package_id}"
          )
            | Перегенерировать
          v-btn(
            color="primary"
            @click="GENERATE_PACKAGE"
          )
            | Сгенерировать пакет
          v-spacer
          v-btn(
            color="primary"
            @click="UPDATE_CONTRAGENT"
          )
            | Сохранить
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { ValidationProvider, ValidationObserver } from 'vee-validate'

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  async asyncData ({ $axios, store, params }) {
    await store.dispatch('contragents/FETCH_CONTRAGENT', params.id)
  },
  data: () => ({}),
  computed: {
    ...mapState({
      contragentInfo: (state) => {
        const data = state.contragents.detail
        const result = Object.keys(data).map((key) => {
          const test = {}
          test[key] = `${data[key]}`
          return test
        })
        return result
      }
    }),
    contragent: {
      get () {
        return this.$store.state.contragents.detail
      },
      set (newValue) {
        // this.$stote.commit('contragents/' + types.SET_CONTRAGENT, newValue)
      }
    },
    panels () {
      return [...Array(this.contragentInfo.length).keys()]
    }
  },
  methods: {
    ...mapActions({
      UPDATE_CONTRAGENT: 'contragents/UPDATE_CONTRAGENT',
      GENERATE_PACKAGE: 'packages/GENERATE_PACKAGE'
    })
  }
}
</script>
