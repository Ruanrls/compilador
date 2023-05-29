export default {
    logo: <span>Documentação, analisador léxico e sintático</span>,
    project: {
      link: 'https://github.com/Ruanrls/compilador'
    },
    search: {
      component: null
    },
    editLink: {
      component: null
    },
    feedback: {
      content: null
    },
    footer: {
      component: null
    },
    useNextSeoProps() {
      return {
        titleTemplate: 'Ruan – %s',
      }
    },
    head: (
      <link rel="shortcut icon" href="/vercel.svg" type="image/ico" />
    )
}