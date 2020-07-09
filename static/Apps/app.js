console.log("BIENVENIDOS A ERALY APP 1.0")

class App extends React.Component {
    render() {
        return (
            <div>
                ©2018 All Rights Reserved. Business Intelligence Thinks
            </div>
        );
    }
}

ReactDOM.render(<App/>, pie);
//
// class PlanCuentas extends React.Component {
//     state = {
//         articulos: null
//     };
//
//     componentWillMount() {
//         fetch('/contabilidad/catalogo/')
//             .then((response) => {
//                 this.state.articulos=response;
//                 console.log(this.state.articulos)
//             })
//     }
//
//     render() {
//         return (
//             <div>
//                 {this.state.articulos}
//             </div>
//         );
//     }
//
// }
// ReactDOM.render(<PlanCuentas/>, pie);