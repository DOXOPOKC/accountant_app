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
          | Контрагент № 1337
        v-card-text
            v-expansion-panels(
              v-model="panels"
              accordion
              multiple
              hover
              flat
              tile
            )
              v-expansion-panel(
                v-for="(item,i) in contragent"
                :key="i"
              )
                v-expansion-panel-header {{ item.title }}
                v-expansion-panel-content
                  //- v-subheader {{ item.name }}
                  v-text-field(v-if="item.name" :label="item.name")
                  v-row(v-if="item.items")
                    v-col(
                      v-for="(date, i) in item.items"
                      :key="i"
                      cols="6")
                      v-subheader(class="pa-0 ma-0") {{ date.title }}
                      v-text-field(
                        :label="date.value")
        v-card-actions(class="px-10 py-6")
          v-spacer
          v-btn(
            color="primary"
            nuxt
            to="/inspire"
          )
            | Continue
</template>

<script>
export default {
  data: () => ({
    test: 'qwe',
    panels: [0, 1, 2],
    contragent: [
      {
        title: 'Тип контрагента',
        name: 'Новоселова Наталья Александровна',
        address: 'Россия, Кемеровская область, Киселёвск, улица Поповича, 5'
      },
      {
        title: 'Физическое лицо',
        id: 113313,
        name: 'Новоселова Наталья Александровна',
        phone: '+7 908 957-62-88'
      },
      {
        title: 'Информация',
        items: [
          {
            title: 'Дата создания',
            value: '2019-12-30'
          },
          {
            title: 'Дата изменения',
            value: '2019-12-30'
          }
        ]
      }
    ]
  })
}
</script>
