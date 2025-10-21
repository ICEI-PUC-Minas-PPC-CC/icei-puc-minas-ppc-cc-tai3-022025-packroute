import { StyleSheet, Dimensions } from "react-native"

const { height } = Dimensions.get('window');

export const styles = StyleSheet.create({
    container: {
        flex: 1,
    },

    map: {
        width: '100%',
        height: height * 0.65, // 65% da tela pro mapa
    },

    floatingButton: {
        position: 'absolute',
        bottom: height * 0.35 + 20, // acima do painel
        right: 20,
        backgroundColor: '#1e3a8a',
        borderRadius: 50,
        padding: 12,
        elevation: 5,
        shadowColor: '#000',
        shadowOpacity: 0.3,
        shadowOffset: { width: 0, height: 2 },
        shadowRadius: 3,
    },

    bottomSheet: {
        position: 'absolute',
        bottom: 0,
        width: '100%',
        height: height * 0.35, // 35% da tela pro painel
        backgroundColor: '#fff',
        borderTopLeftRadius: 20,
        borderTopRightRadius: 20,
        paddingHorizontal: 20,
        paddingTop: 10,
        elevation: 10,
    },

    titulo: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 10,
        color: '#1e3a8a',
    },

    card: {
        backgroundColor: '#f3f4f6',
        padding: 10,
        borderRadius: 12,
        marginBottom: 10,
    },

    cliente: {
        fontSize: 16,
        fontWeight: '600',
    },

    endereco: {
        color: '#4b5563',
    },

    status: {
        color: '#2563eb',
        marginTop: 4,
    },

    loadingText: {
        textAlign: 'center',
        marginTop: 20
    },

    centerButton: {
        position: 'absolute',
        bottom: 90,
        right: 20,
        backgroundColor: '#fff',
        borderRadius: 30,
        padding: 10,
        elevation: 5,
    },

    startButton: {
        position: 'absolute',
        bottom: 20,
        left: 20,
        right: 20,
        backgroundColor: '#2e7d32',
        borderRadius: 10,
        paddingVertical: 15,
        alignItems: 'center',
        elevation: 6,
    },

    startButtonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: '600',
    },

    buttonText: {
        fontSize: 22,
    }
});