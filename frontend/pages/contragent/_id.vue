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
                        v-if="Object.values(item)"
                        :label="Object.values(item)[0]"
                        :error-messages="errors"
                      )
        v-card-actions(class="px-10 py-6")
          v-btn(
            color="primary"
            @click=""
          )
            | Перегенерировать
          v-btn(
            color="primary"
            @click=""
          )
            | Сгенерировать пакет
          v-spacer
          v-btn(
            color="primary"
            @click=""
          )
            | Сохранить
</template>

<script>
import { mapState } from 'vuex'
import { ValidationProvider, ValidationObserver } from 'vee-validate'
import { types } from '~/store/contragents'

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  async asyncData ({ $axios, store, params }) {
    await store.dispatch(`contragents/${types.FETCH_CONTRAGENT}`, params.id)
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
      },
      contragent: state => state.contragents.detail
    }),
    panels () {
      return [...Array(this.contragentInfo.length).keys()]
    }
  },
  methods: {}
}
</script>
