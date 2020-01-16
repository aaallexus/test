export function loadHot() {
    return {
        type: 'LOAD_HOT',
        payload: {
            request: {
             //   url: '',
				method:'POST',
                data:{
                    action:1
                },
/*				params:{
					tre:1
				}*/
            },
        },
    };
}
