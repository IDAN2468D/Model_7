def generate_react_native_component():
    styles = {
        "container": {
            "flex": 1,
            "justifyContent": "center",
            "alignItems": "center",
        },
        "text": {"color": "#ffffff"},
    }

    styles_str = ",\n".join([f'"{key}": {value}' for key, value in styles.items()])

    return f"""
import React from 'react';
import {{ View, Text, StyleSheet }} from 'react-native';

const GeneratedComponent = () => {{
  return (
    <View style={{styles.container}}>
      <Text style={{styles.text}}>GoBack</Text>
    </View>
  );
}}

const styles = StyleSheet.create({{{styles_str}}});

export default GeneratedComponent;
"""
