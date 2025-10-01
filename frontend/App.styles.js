import { StyleSheet } from "react-native"
import { colors } from "./src/styles/colors"

export const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background
    },

    scrollView: {
        flexGrow: 1, 
    },
    
    content:{
        flex: 1, 
        paddingHorizontal: 24,
        paddingTop: 80,
        paddingBottom: 24
    },

    header: {
        marginBottom: 32,
        alignItems: "center",
    },

    title: {
        fontSize: 32,
        fontWeight: 'bold',
        color: colors.text,
        marginBotton: 8,
    },
            
    subTitle: {
        color: colors.textSecondary,
        fontSize: 16
    }, 

    card: {
        backgroundColor: colors.cardBackground,
        borderRadius: 16,
        padding: 24,
        marginBottom: 24
    },

    label: {
        color: colors.textSecondary,
        marginBottom: 8,
        fontSize: 14
    },    
})