import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || ''

export async function analyseResume(file, jobUrls) {
    const form = new FormData()
    form.append('file', file)
    form.append('job_urls', JSON.stringify(jobUrls))

    const { data } = await axios.post(`${BASE}/api/analyse`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120_000,
    })
    return data
}
