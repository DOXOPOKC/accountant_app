<template lang="pug">
    v-app
        v-navigation-drawer(
          app
          v-model="drawer"
          fixed
          clipped
          class="elevation-2"
          mini-variant
          mini-variant-width="64"
          hide-overlay
          dark
        )
            v-row(class="fill-height" no-gutters)
              v-col(cols="12")
                v-navigation-drawer(
                    v-model="drawer"
                    mini-variant
                    mini-variant-width="64"
                    color="primary"
                    class="elevation-0 pt-2"
                    hide-overlay
                )
                    v-list-item
                        v-list-item-avatar
                            //- v-img(src="https://randomuser.me/api/portraits/women/75.jpg")
                            v-icon(class="white black--text") mdi-account
                    v-list(
                        dense
                        nav
                    )
                        v-list-item(
                            v-for="(item, i) in items"
                            :key="i"
                            :to="item.to"
                            router
                            exact
                            flat
                            class="py-3"
                        )
                              v-tooltip(right dark)
                                template(v-slot:activator="{ on }")
                                  v-icon(v-on="on") {{ item.icon }}
                                span {{ item.title }}
              //- v-col(cols="9")
              //-   v-list(class="grow" color="grey lighten-3")
              //-       v-list-item(
              //-           v-for="link in links"
              //-           :key="link"
              //-           link
              //-       )
              //-           v-list-item-title(v-text="link")
        v-app-bar(
            class="elevation-2"
            clipped-left
            app
        )
            v-app-bar-nav-icon(@click.stop="drawer = !drawer")
            v-spacer
            v-icon(color="primary" class="mx-1")
                | M13.7762 1.25867C17.3867 -0.0631387 21.0723 3.02948 20.4104 6.82538L18.6231 17.0743C17.9612 20.8702 13.4481 22.5225 10.4996 20.0484L2.5386 13.3683C-0.409905 10.8942 0.417539 6.14936 4.028 4.82756L13.7762 1.25867Z
            v-toolbar-title(class="text-uppercase headline")
                span(class="primary--text") Эко
                span(class="grey--text text--darken-2") тек
        v-content
            v-container(fluid fill-height pa-0 align-start)
                nuxt
</template>

<script>
export default {
  data: () => ({
    links: ['Home', 'Contacts', 'Settings'],
    clipped: false,
    drawer: true,
    fixed: false,
    items: [
      {
        icon: 'mdi-chart-bubble',
        title: 'Контрагенты',
        to: '/'
      }
    ]
  })
}
</script>

<style scoped>
.v-list .v-list-item--active {
    color: white;
}
</style>
