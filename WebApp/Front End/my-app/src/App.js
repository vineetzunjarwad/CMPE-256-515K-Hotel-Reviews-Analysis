import React, { Component } from 'react';
import './App.css';
import User from './User.js';
import Recommendation from './Recommendation.js'
import { Button } from 'antd';
import { Input } from 'antd';
import ContentHolder from './contentHolder';
import styled from 'styled-components';
import { palette } from 'styled-theme';
import { Row, Col } from 'antd';
import basicStyle from './basicStyle';
import { rtl } from './withDirection';
import Box from './box';
import LayoutWrapper from './layoutWrapper.js';

const { rowStyle, colStyle, gutter } = basicStyle;
      const marginStyle = {
        margin: rtl === 'rtl' ? '10px 10px 10px 10px' : '10px 10px 10px 10px'
      };

class App extends Component {

  state = {
      suggestions :[],
      recommendations:[],
      cityName:'',
      countryName:''
  }

  handleCityChange = (event)=>{
   this.setState({cityName:event.target.value})
  }

  handleCountryChange = (event)=>{
   this.setState({countryName:event.target.value})
  }

  showRecommendations = (name) =>{

    fetch('http://127.0.0.1:5000/recommendations?hotelName='+name)
            .then((response)=>{return response.json()}).then((data)=>{
               console.log(data);
               this.setState({recommendations:data})
            });

  }

  handleSubmit = (event)=>{

            event.preventDefault();
            let cityInput = event.target[0].value;
            let countryInput = event.target[1].value;
            console.log(cityInput)
            this.setState({cityName:cityInput})
            this.setState({countryName:countryInput})

              fetch('http://127.0.0.1:5000/suggestions?nationality='+countryInput+'&city='+cityInput)
                      .then((response)=>{return response.json()}).then((data)=>{
                         console.log(data);
                          let list = []
                         for (let i in data)
                          list.push(data[i]);

                         this.setState({suggestions:list})
                      });
    }


  render() {

    return (
      <div className="App">
       <h1>Hotel Search</h1>
        <form className = "Form" ref="form" onSubmit={this.handleSubmit}>
            <div className ="InputText">
            <span style = {{paddingRight:'20px'}}> Location: </span>
            <input className ="InputText" placeholder="City Name" type="text" name="cityname" value={this.state.cityName} onChange={this.handleCityChange} />
             </div>
             <div className ="InputText">
             <span style = {{paddingRight:'20px'}}> Nationality: </span>
            <input  className ="InputText" placeholder="Nationality" type="text" name="nationality" value={this.state.countryName} onChange={this.handleCountryChange}></input>
            </div>
            <div>
            <button style = {{fontSize:'20px'}} type="submit">Search Top Reviewed Hotels</button>
            </div>
        </form>

        <User suggestionlist= {this.state.suggestions}  hotelList ={this.showRecommendations}></User>

        <Recommendation recommendList={this.state.recommendations}></Recommendation>

      </div>
    );
  }
}

export default App;
