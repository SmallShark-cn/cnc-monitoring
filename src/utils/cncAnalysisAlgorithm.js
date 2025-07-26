/**
 * CNC刀具磨损智能检测算法
 * 基于振动、温度、声学多传感器融合分析
 */

export default class CNCAnalysisAlgorithm {
  constructor() {
    // 阈值配置
    this.thresholds = {
      temperature: {
        normal: 25,     // 正常温度阈值
        high: 35        // 高温阈值
      },
      vibration: {
        rms: {
          normal: 0.3,    // RMS正常阈值
          warning: 0.6,   // RMS告警阈值
          critical: 1.0   // RMS危险阈值
        },
        kurtosis: {
          normal: 4,      // 峭度正常阈值
          warning: 6,     // 峭度告警阈值
          critical: 8     // 峭度危险阈值
        },
        peak: {
          normal: 0.8,    // 峰值正常阈值
          warning: 1.5,   // 峰值告警阈值
          critical: 2.5   // 峰值危险阈值
        }
      },
      acoustic: {
        spl: {
          normal: 80,     // SPL正常阈值
          warning: 90,    // SPL告警阈值
          critical: 100   // SPL危险阈值
        },
        rms: {
          normal: 0.2,    // 声学RMS正常阈值
          warning: 0.4,   // 声学RMS告警阈值
          critical: 0.6   // 声学RMS危险阈值
        }
      }
    }
    
    // 权重配置
    this.weights = {
      vibration: 0.5,   // 振动权重
      temperature: 0.3, // 温度权重
      acoustic: 0.2     // 声学权重
    }
    
    // 历史数据缓存
    this.historySize = 10
    this.vibrationHistory = []
    this.temperatureHistory = []
    this.acousticHistory = []
  }

  /**
   * 更新历史数据
   */
  updateHistory(vibrationData, temperatureData, acousticData) {
    // 更新振动历史
    if (vibrationData) {
      this.vibrationHistory.unshift(vibrationData)
      if (this.vibrationHistory.length > this.historySize) {
        this.vibrationHistory.pop()
      }
    }

    // 更新温度历史
    if (temperatureData !== null && temperatureData !== undefined) {
      this.temperatureHistory.unshift(temperatureData)
      if (this.temperatureHistory.length > this.historySize) {
        this.temperatureHistory.pop()
      }
    }

    // 更新声学历史
    if (acousticData) {
      this.acousticHistory.unshift(acousticData)
      if (this.acousticHistory.length > this.historySize) {
        this.acousticHistory.pop()
      }
    }
  }

  /**
   * 振动分析
   */
  analyzeVibration(vibrationData) {
    if (!vibrationData) return { score: 0, level: 'normal', details: '无振动数据' }

    const rms = vibrationData.rms || 0
    const kurtosis = vibrationData.kurtosis || 0
    const peak = vibrationData.peak || 0

    let score = 0
    let level = 'normal'
    let details = []

    // 更敏感的RMS分析（降低阈值以便演示异常状态）
    if (rms > this.thresholds.vibration.rms.critical * 0.6) {
      score += 35
      level = 'critical'
      details.push(`RMS异常高 (${rms.toFixed(3)})`)
    } else if (rms > this.thresholds.vibration.rms.warning * 0.5) {
      score += 20
      level = 'warning'
      details.push(`RMS偏高 (${rms.toFixed(3)})`)
    } else if (rms > 0.3) { // 新增：轻微异常检测
      score += 12
      details.push(`RMS轻微偏高 (${rms.toFixed(3)})`)
    }

    // 更敏感的峭度分析
    if (kurtosis > this.thresholds.vibration.kurtosis.critical * 0.7) {
      score += 30
      level = 'critical'
      details.push(`峭度异常 (${kurtosis.toFixed(2)})`)
    } else if (kurtosis > this.thresholds.vibration.kurtosis.warning * 0.6) {
      score += 15
      details.push(`峭度偏高 (${kurtosis.toFixed(2)})`)
    } else if (kurtosis > 4.0 || kurtosis < 2.5) { // 新增：轻微异常检测
      score += 10
      details.push(`峭度轻微异常 (${kurtosis.toFixed(2)})`)
    }

    // 更敏感的峰值分析
    if (peak > this.thresholds.vibration.peak.critical * 0.6) {
      score += 25
      level = 'critical'
      details.push(`峰值过高 (${peak.toFixed(3)})`)
    } else if (peak > this.thresholds.vibration.peak.warning * 0.5) {
      score += 12
      details.push(`峰值偏高 (${peak.toFixed(3)})`)
    } else if (peak > 0.8) { // 新增：轻微异常检测
      score += 8
      details.push(`峰值轻微偏高 (${peak.toFixed(3)})`)
    }

    // 趋势分析
    if (this.vibrationHistory.length >= 3) {
      const recentRMS = this.vibrationHistory.slice(0, 3).map(d => d.rms || 0)
      const trend = this.calculateTrend(recentRMS)
      if (trend > 0.1) {
        score += 10
        details.push('振动呈上升趋势')
      }
    }

    return {
      score: Math.min(score, 100),
      level: score > 50 ? 'critical' : (score > 20 ? 'warning' : 'normal'),
      details: details.join(', ') || '振动正常',
      metrics: { rms, kurtosis, peak }
    }
  }

  /**
   * 温度分析
   */
  analyzeTemperature(temperature) {
    if (temperature === null || temperature === undefined) {
      return { score: 0, level: 'normal', details: '无温度数据' }
    }

    let score = 0
    let level = 'normal'
    let details = []

    // 更敏感的温度分析（降低阈值以便演示异常状态）
    if (temperature > this.thresholds.temperature.high * 0.8) {
      score = 85
      level = 'critical'
      details.push(`温度过高 (${temperature.toFixed(1)}°C)`)
    } else if (temperature > this.thresholds.temperature.normal * 0.7) {
      score = 35
      level = 'warning'  
      details.push(`温度偏高 (${temperature.toFixed(1)}°C)`)
    } else if (temperature > 22) { // 新增：轻微异常检测
      score = 20
      details.push(`温度轻微偏高 (${temperature.toFixed(1)}°C)`)
    }

    // 温度趋势分析
    if (this.temperatureHistory.length >= 3) {
      const trend = this.calculateTrend(this.temperatureHistory.slice(0, 3))
      if (trend > 2) {
        score += 15
        details.push('温度快速上升')
      }
    }

    return {
      score: Math.min(score, 100),
      level: score > 60 ? 'critical' : (score > 25 ? 'warning' : 'normal'),
      details: details.join(', ') || '温度正常',
      metrics: { temperature }
    }
  }

  /**
   * 声学分析
   */
  analyzeAcoustic(acousticData) {
    if (!acousticData) return { score: 0, level: 'normal', details: '无声学数据' }

    const spl = acousticData.spl || 0
    const rms = acousticData.rms || 0
    const kurtosis = acousticData.kurtosis || 0

    let score = 0
    let level = 'normal'
    let details = []

    // 更敏感的SPL分析（降低阈值以便演示异常状态）
    if (spl > this.thresholds.acoustic.spl.critical * 0.7) {
      score += 30
      level = 'critical'
      details.push(`噪声过高 (${spl.toFixed(1)}dB)`)
    } else if (spl > this.thresholds.acoustic.spl.warning * 0.6) {
      score += 18
      level = 'warning'
      details.push(`噪声偏高 (${spl.toFixed(1)}dB)`)
    } else if (spl > 70) { // 新增：轻微异常检测
      score += 12
      details.push(`噪声轻微偏高 (${spl.toFixed(1)}dB)`)
    }

    // 更敏感的声学RMS分析
    if (rms > this.thresholds.acoustic.rms.critical * 0.6) {
      score += 25
      level = 'critical'
      details.push(`声学能量异常 (${rms.toFixed(3)})`)
    } else if (rms > this.thresholds.acoustic.rms.warning * 0.5) {
      score += 15
      details.push(`声学能量偏高 (${rms.toFixed(3)})`)
    } else if (rms > 0.3) { // 新增：轻微异常检测
      score += 10
      details.push(`声学能量轻微偏高 (${rms.toFixed(3)})`)
    }

    // 峭度分析（声学）
    if (kurtosis > 5.0) {
      score += 15
      details.push(`声学峭度异常 (${kurtosis.toFixed(2)})`)
    } else if (kurtosis > 4.5 || kurtosis < 2.0) {
      score += 8
      details.push(`声学峭度轻微异常 (${kurtosis.toFixed(2)})`)
    }

    return {
      score: Math.min(score, 100),
      level: score > 40 ? 'critical' : (score > 15 ? 'warning' : 'normal'),
      details: details.join(', ') || '声学正常',
      metrics: { spl, rms, kurtosis }
    }
  }

  /**
   * 综合分析
   */
  comprehensiveAnalysis(vibrationData, temperature, acousticData) {
    // 更新历史数据
    this.updateHistory(vibrationData, temperature, acousticData)

    // 各传感器分析
    const vibrationAnalysis = this.analyzeVibration(vibrationData)
    const temperatureAnalysis = this.analyzeTemperature(temperature)
    const acousticAnalysis = this.analyzeAcoustic(acousticData)

    // 加权综合评分
    const totalScore = 
      vibrationAnalysis.score * this.weights.vibration +
      temperatureAnalysis.score * this.weights.temperature +
      acousticAnalysis.score * this.weights.acoustic

    // 综合状态判断
    let overallLevel = 'normal'
    let overallStatus = '正常'
    let temperatureStatus = '正常'
    
    if (totalScore > 60) {
      overallLevel = 'critical'
      overallStatus = '异常'
    } else if (totalScore > 30) {
      overallLevel = 'warning'
      overallStatus = '异常'
    }

    // 温度状态判断
    if (temperature > this.thresholds.temperature.high) {
      temperatureStatus = '高温'
    }

    // 刀具磨损预测
    const wearPrediction = this.predictToolWear(vibrationAnalysis, temperatureAnalysis, acousticAnalysis, totalScore)

    // 生成告警
    const alerts = this.generateAlerts(vibrationAnalysis, temperatureAnalysis, acousticAnalysis, overallLevel)

    return {
      overall: {
        score: totalScore,
        level: overallLevel,
        status: overallStatus,
        temperatureStatus: temperatureStatus
      },
      vibration: vibrationAnalysis,
      temperature: temperatureAnalysis,
      acoustic: acousticAnalysis,
      toolWear: wearPrediction,
      alerts: alerts,
      timestamp: new Date().toISOString()
    }
  }

  /**
   * 刀具磨损预测
   */
  predictToolWear(vibrationAnalysis, temperatureAnalysis, acousticAnalysis, totalScore) {
    let wearState = 'normal'
    let confidence = 0.7
    let rul = 1000 // 剩余使用寿命（小时）

    // 更敏感的异常检测逻辑
    const vibrationScore = vibrationAnalysis.score || 0
    const temperatureScore = temperatureAnalysis.score || 0
    const acousticScore = acousticAnalysis.score || 0
    
    // 单传感器异常阈值检测
    const vibrationThreshold = vibrationScore > 15 // 振动异常阈值降低
    const temperatureThreshold = temperatureScore > 25 // 温度异常阈值
    const acousticThreshold = acousticScore > 20 // 声学异常阈值
    
    // 多传感器融合异常检测
    const multiSensorAbnormal = (vibrationThreshold && temperatureThreshold) || 
                               (vibrationThreshold && acousticThreshold) ||
                               (temperatureThreshold && acousticThreshold)
    
    // 基于综合评分和多传感器融合判断磨损状态
    if (totalScore > 60 || multiSensorAbnormal) {
      wearState = 'severe'
      confidence = 0.92
      rul = Math.max(20, 150 - totalScore * 2)
    } else if (totalScore > 35 || vibrationThreshold || temperatureThreshold) {
      wearState = 'moderate'
      confidence = 0.85
      rul = Math.max(100, 500 - totalScore * 6)
    } else if (totalScore > 15 || acousticThreshold) {
      wearState = 'slight'
      confidence = 0.78
      rul = Math.max(300, 750 - totalScore * 10)
    }
    
    // 动态调整置信度
    if (multiSensorAbnormal) {
      confidence = Math.min(0.95, confidence + 0.1)
    }

    // 计算各传感器贡献度
    const totalContribution = vibrationAnalysis.score + temperatureAnalysis.score + acousticAnalysis.score
    const contributions = {
      vibration: totalContribution > 0 ? (vibrationAnalysis.score / totalContribution).toFixed(2) : 0,
      acoustic: totalContribution > 0 ? (acousticAnalysis.score / totalContribution).toFixed(2) : 0,
      temperature: totalContribution > 0 ? (temperatureAnalysis.score / totalContribution).toFixed(2) : 0
    }

    return {
      wear_state: wearState,
      confidence: confidence,
      rul: Math.round(rul),
      contributions: contributions
    }
  }

  /**
   * 生成告警信息
   */
  generateAlerts(vibrationAnalysis, temperatureAnalysis, acousticAnalysis, overallLevel) {
    const alerts = []
    const currentTime = new Date().toLocaleString('zh-CN')

    // 温度告警
    if (temperatureAnalysis.level === 'critical') {
      alerts.push({
        type: '温度',
        time: currentTime,
        message: temperatureAnalysis.details
      })
    }

    // 振动告警
    if (vibrationAnalysis.level === 'critical') {
      alerts.push({
        type: '振动',
        time: currentTime,
        message: vibrationAnalysis.details
      })
    }

    // 声学告警
    if (acousticAnalysis.level === 'critical') {
      alerts.push({
        type: '声学',
        time: currentTime,
        message: acousticAnalysis.details
      })
    }

    // 综合状态告警
    if (overallLevel === 'critical') {
      alerts.push({
        type: '系统',
        time: currentTime,
        message: '检测到多项异常指标，建议立即检查设备'
      })
    }

    return alerts
  }

  /**
   * 计算趋势
   */
  calculateTrend(values) {
    if (values.length < 2) return 0
    
    let trend = 0
    for (let i = 1; i < values.length; i++) {
      trend += values[i-1] - values[i]
    }
    return trend / (values.length - 1)
  }

  /**
   * 重置历史数据
   */
  resetHistory() {
    this.vibrationHistory = []
    this.temperatureHistory = []
    this.acousticHistory = []
  }
}