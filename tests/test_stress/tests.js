import http from 'k6/http';
import {check} from 'k6';

export let options = {
    stages: [
        {duration: '20s', target: 10}, // 1000 виртуальных пользователей в течение 1 минуты
        // {duration: '2m', target: 50}, // поддерживаем 1000 пользователей в течение 2 минут
    ],
};
export default function () {
    let res = http.get('http://localhost:8000/api/info', {
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3Mzk1MzEwOTB9.dXbtnAPvuyJnAKMPDwkqX6PPclusd2Ez38eAznBE8PQ'
        }

    });
    // let res = http.post('http://localhost:8000/api/auth', JSON.stringify({
    //     username: 'test2',
    //     password: 'test2',
    // }), {
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'accept': 'application/json'
    //     }
    // });

    check(res, {
        'is status 200': (r) => r.status === 200,
    });
}