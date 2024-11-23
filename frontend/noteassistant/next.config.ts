// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://ec2-18-246-27-158.us-west-2.compute.amazonaws.com:5111/:path*',
      },
    ]
  },
};
