def generate_react_native_component():
    styles = {
        "container": {
            "flex": 1,
            "justifyContent": "center",
            "alignItems": "center",
        },
        "text": {"color": "#ffffff"},
        "myComponentContainer": {
            "marginTop": 20,
            "padding": 10,
            "backgroundColor": "#333",
        },
        "myComponentText": {
            "color": "blue",
        },
    }

    styles_str = ",\n".join([f'"{key}": {value}' for key, value in styles.items()])

    return f"""
import React from 'react';
import {{ View, Text, StyleSheet }} from 'react-native';

const MyComponent = () => {{
  return (
    <View style={{styles.myComponentContainer}}>
      <Text style={{styles.myComponentText}}>Hello from MyComponent!</Text>
    </View>
  );
}}

const GeneratedComponent = () => {{
  return (
    <View style={{styles.container}}>
      <Text style={{styles.text}}>GoBack</Text>
      <MyComponent />
    </View>
  );
}}

const styles = StyleSheet.create({{{styles_str}}});

export default GeneratedComponent;
"""
